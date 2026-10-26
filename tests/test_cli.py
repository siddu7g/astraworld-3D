import unittest

from apps.api.cli import build_parser


class CliTests(unittest.TestCase):
    def test_cli_has_worldforge_prog_name(self) -> None:
        parser = build_parser()
        self.assertEqual(parser.prog, "worldforge")

    def test_cli_help_mentions_public_commands(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        for command in ("generate", "world", "export", "to-isaac", "marble-to-isaac", "credits"):
            self.assertIn(command, help_text)

    def test_to_isaac_accepts_world_id_or_ply(self) -> None:
        parser = build_parser()
        to_parser = None
        for action in parser._actions:
            if getattr(action, "dest", None) == "command":
                to_parser = action.choices.get("to-isaac")  # type: ignore[attr-defined]
                break
        self.assertIsNotNone(to_parser)
        to_help = to_parser.format_help()  # type: ignore[union-attr]
        self.assertIn("--ply", to_help)
        self.assertIn("--world-id", to_help)

    def test_hidden_compatibility_flags_are_not_in_help(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        self.assertNotIn("--draft-only", help_text)
        self.assertNotIn("--no-plus", help_text)


if __name__ == "__main__":
    unittest.main()
