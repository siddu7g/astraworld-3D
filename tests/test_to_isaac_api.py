import unittest
from unittest.mock import patch

from isaac_ready.to_isaac import to_isaac


class ToIsaacApiTests(unittest.TestCase):
    def test_requires_exactly_one_source(self) -> None:
        with self.assertRaises(ValueError):
            to_isaac()
        with self.assertRaises(ValueError):
            to_isaac(ply="a.ply", world_id="abc")

    def test_ply_path_delegates_to_converter(self) -> None:
        with patch("isaac_ready.to_isaac.convert_ply_to_isaac") as mocked:
            mocked.return_value = "ok"
            out = to_isaac(ply="/tmp/demo.ply", profile="100k", scene_name="demo", out_dir="/tmp/out")
            self.assertEqual(out, "ok")
            mocked.assert_called_once()
            kwargs = mocked.call_args.kwargs
            self.assertEqual(kwargs["profile_name"], "100k")
            self.assertEqual(kwargs["scene_name"], "demo")


if __name__ == "__main__":
    unittest.main()
