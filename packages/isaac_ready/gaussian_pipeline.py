"""Gaussian splat PLY -> Isaac Sim NuRec stage conversion.

Works for World Labs Marble exports and other binary little-endian 3DGS PLYs
that carry the common float properties (x/y/z, scales, rotations, opacity, SH).
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from isaac_ready.paths import isaac_sim_path


@dataclass(frozen=True)
class GaussianProfile:
    name: str
    target_count: int | None
    clip_nonfinite: bool


@dataclass(frozen=True)
class ConversionResult:
    """Public result of a PLY -> Isaac conversion."""

    view_usda: Path
    out_dir: Path
    sanitized_ply: Path
    usdz: Path
    gaussian_count: int
    profile: str
    source_ply: Path
    open_command: str


PROFILES: dict[str, GaussianProfile] = {
    "100k": GaussianProfile(name="100k", target_count=100_000, clip_nonfinite=False),
    "fullish": GaussianProfile(name="fullish", target_count=300_000, clip_nonfinite=False),
    "500k": GaussianProfile(name="500k", target_count=500_000, clip_nonfinite=True),
}


def convert_ply_to_isaac_stage(
    ply_path: Path | str,
    *,
    out_dir: Path | str,
    profile_name: str = "fullish",
    scene_name: str | None = None,
) -> Path:
    """
    Convert any compatible Gaussian splat PLY into an Isaac-openable NuRec stage.

    Returns the path to `stage/view.usda` (open this file, not default.usda).
    """
    return convert_ply_to_isaac(ply_path, out_dir=out_dir, profile_name=profile_name, scene_name=scene_name).view_usda


def convert_ply_to_isaac(
    ply_path: Path | str,
    *,
    out_dir: Path | str,
    profile_name: str = "fullish",
    scene_name: str | None = None,
) -> ConversionResult:
    """
    Convert a Gaussian splat PLY into an Isaac-openable NuRec stage.

    Accepts:
      - World Labs / Marble PLY exports
      - Other binary little-endian 3DGS PLYs with float vertex properties

    Output layout:
      out_dir/
        <scene_name>.ply
        <scene_name>.usdz
        conversion_summary.txt
        stage/
          default.usda
          gauss.usda
          <scene_name>.nurec
          view.usda   # open this in Isaac
    """
    if profile_name not in PROFILES:
        raise ValueError(f"Unknown profile '{profile_name}'. Choose from: {', '.join(sorted(PROFILES))}")

    profile = PROFILES[profile_name]
    ply_path = Path(ply_path).expanduser().resolve()
    out_dir = Path(out_dir).expanduser().resolve()
    scene_name = scene_name or _slugify(ply_path.stem)
    if not ply_path.is_file():
        raise FileNotFoundError(f"PLY not found: {ply_path}")

    out_dir.mkdir(parents=True, exist_ok=True)
    stage_dir = out_dir / "stage"
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True, exist_ok=True)

    clean_ply = out_dir / f"{scene_name}.ply"
    usdz_path = out_dir / f"{scene_name}.usdz"

    count = sanitize_gaussian_ply(
        ply_path,
        clean_ply,
        target_count=profile.target_count,
        clip_nonfinite=profile.clip_nonfinite,
    )
    _run_3dgrut_convert(clean_ply, usdz_path)
    _extract_usdz(usdz_path, stage_dir)
    view_usda = stage_dir / "view.usda"
    _write_view_stage(view_usda)

    meta = out_dir / "conversion_summary.txt"
    open_cmd = build_open_command(view_usda)
    meta.write_text(
        "\n".join(
            [
                f"source_ply={ply_path}",
                f"profile={profile.name}",
                f"gaussian_count={count}",
                f"sanitized_ply={clean_ply}",
                f"usdz={usdz_path}",
                f"open_this={view_usda}",
                f"open_command={open_cmd}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return ConversionResult(
        view_usda=view_usda,
        out_dir=out_dir,
        sanitized_ply=clean_ply,
        usdz=usdz_path,
        gaussian_count=count,
        profile=profile.name,
        source_ply=ply_path,
        open_command=open_cmd,
    )


def sanitize_gaussian_ply(
    src: Path | str,
    dst: Path | str,
    *,
    target_count: int | None,
    clip_nonfinite: bool,
) -> int:
    """
    Sanitize a binary little-endian Gaussian splat PLY for Isaac / 3DGRUT.

    - drops non-finite vertices (or clips them when clip_nonfinite=True)
    - clamps opacity logits into a stable range
    - optionally downsamples to target_count
    - strips unused normals (nx/ny/nz)
    """
    src = Path(src)
    dst = Path(dst)
    raw = src.read_bytes()
    header_end = raw.find(b"end_header\n")
    if header_end < 0:
        header_end = raw.find(b"end_header\r\n")
        header_sep = b"end_header\r\n"
    else:
        header_sep = b"end_header\n"
    if header_end < 0:
        raise RuntimeError(f"Unsupported PLY header in {src}")

    header = raw[:header_end].decode("latin1")
    payload = raw[header_end + len(header_sep) :]

    props: list[str] = []
    vertex_count: int | None = None
    fmt = None
    for line in header.splitlines():
        line = line.strip()
        if line.startswith("format "):
            fmt = line.split(None, 1)[1]
        elif line.startswith("element vertex"):
            vertex_count = int(line.split()[-1])
        elif line.startswith("property float") or line.startswith("property float32"):
            props.append(line.split()[-1])
    if vertex_count is None:
        raise RuntimeError(f"Could not find element vertex in {src}")
    if not props:
        raise RuntimeError(f"No float vertex properties found in {src}")
    if fmt and "binary_little_endian" not in fmt:
        raise RuntimeError(
            f"Unsupported PLY format '{fmt}' in {src}. "
            "Expected binary_little_endian 3DGS PLY (Marble / standard 3DGS export)."
        )

    expected = vertex_count * len(props) * 4
    if len(payload) < expected:
        raise RuntimeError(
            f"PLY payload too small in {src}: got {len(payload)} bytes, expected >= {expected}"
        )

    arr = np.frombuffer(payload[:expected], dtype=np.float32).reshape(vertex_count, len(props)).copy()
    idx = {name: i for i, name in enumerate(props)}

    if clip_nonfinite:
        for name in props:
            col = arr[:, idx[name]]
            bad = ~np.isfinite(col)
            if bad.any():
                fixed = col.copy()
                fixed[bad] = 0.0
                arr[:, idx[name]] = fixed
    else:
        keep = np.ones(len(arr), dtype=bool)
        for name in props:
            keep &= np.isfinite(arr[:, idx[name]])
        arr = arr[keep]

    if "opacity" in idx:
        arr[:, idx["opacity"]] = np.clip(arr[:, idx["opacity"]], -8.0, 8.0)

    if target_count is not None and len(arr) > target_count:
        rng = np.random.default_rng(42)
        if "opacity" in idx:
            op = arr[:, idx["opacity"]]
            weights = np.clip(op - float(op.min()) + 1e-3, 1e-3, None)
            weights = weights / weights.sum()
            sel = rng.choice(len(arr), size=target_count, replace=False, p=weights)
        else:
            sel = rng.choice(len(arr), size=target_count, replace=False)
        arr = arr[sel]

    keep_props = [name for name in props if name not in {"nx", "ny", "nz"}]
    arr = arr[:, [idx[name] for name in keep_props]]

    dst.parent.mkdir(parents=True, exist_ok=True)
    new_header = "\n".join(
        [
            "ply",
            "format binary_little_endian 1.0",
            f"element vertex {len(arr)}",
            *[f"property float {name}" for name in keep_props],
            "end_header\n",
        ]
    )
    dst.write_bytes(new_header.encode("ascii") + arr.astype(np.float32).tobytes())
    return int(len(arr))


# Backward-compatible alias
sanitize_marble_ply = sanitize_gaussian_ply


def _run_3dgrut_convert(clean_ply: Path, usdz_path: Path) -> None:
    script = isaac_sim_path() / "sim" / "convert_ply_to_usd.sh"
    if not script.is_file():
        raise FileNotFoundError(
            f"Missing 3DGRUT helper: {script}. "
            "Set ISAAC_SIM_PATH to your Isaac Sim install."
        )
    subprocess.run(
        [str(script), str(clean_ply), "-o", str(usdz_path), "-f", "nurec"],
        check=True,
        env={**os.environ},
    )


def _extract_usdz(usdz_path: Path, stage_dir: Path) -> None:
    with zipfile.ZipFile(usdz_path) as archive:
        archive.extractall(stage_dir)


def _write_view_stage(path: Path) -> None:
    path.write_text(
        """#usda 1.0
(
    defaultPrim = "World"
    metersPerUnit = 1
    upAxis = "Z"
    subLayers = [ @gauss.usda@ ]
    customLayerData = {
        dictionary renderSettings = {
            int "rtx:directLighting:sampledLighting:samplesPerPixel" = 1
            bool "rtx:ecoMode:enabled" = 0
            string "rtx:rendermode" = "RaytracedLighting"
        }
    }
)

over "World"
{
    def Camera "ViewerCamera"
    {
        float2 clippingRange = (0.05, 500)
        float focalLength = 18
        double3 xformOp:translate = (5, 3, 2.5)
        float3 xformOp:rotateXYZ = (-20, 55, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]
    }

    def DomeLight "Dome"
    {
        float inputs:intensity = 1200
    }
}
""",
        encoding="utf-8",
    )


def _slugify(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in value.lower())
    return "-".join(part for part in cleaned.split("-") if part) or "scene"


def build_open_command(view_usda: Path | str) -> str:
    view_usda = Path(view_usda).expanduser().resolve()
    return f"{isaac_sim_path() / 'sim' / 'open_gaussian.sh'} {view_usda}"


def add_conversion_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ply", default=None, help="Path to a Gaussian splat PLY (Marble or other 3DGS)")
    parser.add_argument(
        "--profile",
        default="fullish",
        choices=sorted(PROFILES),
        help="Sanitization/size profile: 100k, fullish, or 500k",
    )
    parser.add_argument("--out-dir", default=None, help="Output directory (default under APP_DATA_DIR/gaussian)")
    parser.add_argument("--scene-name", default=None, help="Optional scene name for output files")
