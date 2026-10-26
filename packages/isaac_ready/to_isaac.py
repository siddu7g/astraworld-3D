"""One-shot bridge: Marble world_id or any Gaussian PLY -> Isaac view.usda."""

from __future__ import annotations

import os
from pathlib import Path

from isaac_ready.gaussian_pipeline import ConversionResult, convert_ply_to_isaac


def to_isaac(
    *,
    ply: Path | str | None = None,
    world_id: str | None = None,
    profile: str = "fullish",
    scene_name: str | None = None,
    out_dir: Path | str | None = None,
    resolution: str = "full_res",
    export_mesh: bool = False,
    data_dir: Path | str | None = None,
) -> ConversionResult:
    """
    Convert any Marble world (or any compatible Gaussian PLY) into an Isaac stage.

    Provide exactly one of:
      - ply: local path to a .ply splat export
      - world_id: Marble / World Labs world id (exports PLY then converts)

    Examples:
      to_isaac(ply="~/Downloads/world.ply", profile="fullish")
      to_isaac(world_id="7c74cab4-...", resolution="full_res", profile="fullish")
    """
    if bool(ply) == bool(world_id):
        raise ValueError("Provide exactly one of ply=... or world_id=...")

    root = Path(data_dir or os.environ.get("APP_DATA_DIR", "./data")).expanduser().resolve()

    if world_id:
        ply_path, scene = _export_marble_world(
            world_id=world_id,
            resolution=resolution,
            export_mesh=export_mesh,
            root=root,
            scene_name=scene_name,
        )
        scene_name = scene_name or scene
        out = Path(out_dir) if out_dir else (root / "gaussian" / (scene_name or _slug(world_id)))
        return convert_ply_to_isaac(
            ply_path,
            out_dir=out,
            profile_name=profile,
            scene_name=scene_name,
        )

    ply_path = Path(ply).expanduser().resolve()  # type: ignore[arg-type]
    scene_name = scene_name or _slug(ply_path.stem)
    out = Path(out_dir) if out_dir else (root / "gaussian" / scene_name)
    return convert_ply_to_isaac(
        ply_path,
        out_dir=out,
        profile_name=profile,
        scene_name=scene_name,
    )


def _export_marble_world(
    *,
    world_id: str,
    resolution: str,
    export_mesh: bool,
    root: Path,
    scene_name: str | None,
) -> tuple[Path, str]:
    from look_agent.config import LookConfig
    from look_agent.marble_client import MarbleClient
    from look_agent.polish import polish_and_export

    cfg = LookConfig.from_env()
    cfg.require_marble_key()
    name = scene_name or _slug(world_id)
    export_dir = root / "worlds" / f"export_{name}"
    with MarbleClient(cfg) as client:
        world = client.get_world(world_id)
        result = polish_and_export(
            client,
            world=world,
            out_dir=export_dir,
            export_mesh=export_mesh,
            splat_resolution=resolution,
        )
    ply = (result.get("exports") or {}).get("ply")
    if not ply:
        raise RuntimeError(
            f"Marble world {world_id} did not yield a PLY export. "
            f"See {export_dir / 'export_error.txt'} if present."
        )
    return Path(ply), name


def _slug(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in value.lower())
    return "-".join(part for part in cleaned.split("-") if part)[:48] or "scene"
