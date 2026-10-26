import struct
import tempfile
import unittest
from pathlib import Path

from isaac_ready.gaussian_pipeline import sanitize_gaussian_ply


def _write_tiny_ply(path: Path, *, with_inf: bool = False) -> None:
    # Minimal 3DGS-like binary PLY: xyz + opacity
    props = ["x", "y", "z", "opacity"]
    rows = [
        [0.0, 0.0, 0.0, 0.5],
        [1.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, float("inf") if with_inf else 0.2],
        [0.0, 0.0, 1.0, -0.1],
    ]
    header = "\n".join(
        [
            "ply",
            "format binary_little_endian 1.0",
            f"element vertex {len(rows)}",
            *[f"property float {p}" for p in props],
            "end_header\n",
        ]
    )
    payload = b"".join(struct.pack("<4f", *row) for row in rows)
    path.write_bytes(header.encode("ascii") + payload)


class GaussianPipelineTests(unittest.TestCase):
    def test_sanitize_drops_nonfinite_opacity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src.ply"
            dst = Path(tmp) / "dst.ply"
            _write_tiny_ply(src, with_inf=True)
            count = sanitize_gaussian_ply(src, dst, target_count=None, clip_nonfinite=False)
            self.assertEqual(count, 3)
            self.assertTrue(dst.is_file())

    def test_sanitize_downsamples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src.ply"
            dst = Path(tmp) / "dst.ply"
            _write_tiny_ply(src, with_inf=False)
            count = sanitize_gaussian_ply(src, dst, target_count=2, clip_nonfinite=False)
            self.assertEqual(count, 2)

    def test_sanitize_rejects_ascii(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "ascii.ply"
            dst = Path(tmp) / "dst.ply"
            src.write_text(
                "\n".join(
                    [
                        "ply",
                        "format ascii 1.0",
                        "element vertex 1",
                        "property float x",
                        "property float y",
                        "property float z",
                        "end_header",
                        "0 0 0",
                        "",
                    ]
                ),
                encoding="ascii",
            )
            with self.assertRaises(RuntimeError):
                sanitize_gaussian_ply(src, dst, target_count=None, clip_nonfinite=False)


if __name__ == "__main__":
    unittest.main()
