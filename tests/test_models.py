import unittest

from look_agent.brief import WorldBrief
from site_spec import SiteSpec


class ModelTests(unittest.TestCase):
    def test_world_brief_job_id_uses_display_name_and_seed(self) -> None:
        brief = WorldBrief(
            prompt="Walkable industrial yard with puddles",
            display_name="Industrial Yard",
            region="generic",
            seed=11,
        )
        self.assertEqual(brief.job_id(), "marble_industrial-yard_s11")

    def test_site_spec_site_id_reflects_dimensions(self) -> None:
        spec = SiteSpec(region="americas", seed=42, plot_m=(40.0, 60.0))
        self.assertEqual(spec.site_id(), "americas_s42_40x60")


if __name__ == "__main__":
    unittest.main()
