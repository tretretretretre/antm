import importlib.util
import os
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "render_daily.py"


def load_script_module():
    spec = importlib.util.spec_from_file_location("render_daily", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RenderDailyTest(unittest.TestCase):
    def test_presenter_references_follow_the_episode_configuration(self):
        """Catches the renderer falling back to nonexistent girl1-style paths."""
        module = load_script_module()
        resolver = getattr(
            module,
            "presenter_images_dir",
            lambda episode: module.BASE / "assets" / "characters" / episode["girl"],
        )

        result = resolver(
            {
                "girl": "girl1",
                "presenter_images": "assets/characters/girl3-Siobhan",
            }
        )

        self.assertEqual(REPO / "assets/characters/girl3-Siobhan", result)

    def test_production_assets_resolve_to_files_that_exist(self):
        """Catches stale placeholder logo and intro paths."""
        module = load_script_module()
        resolver = getattr(
            module,
            "production_assets",
            lambda: {
                "brand": module.BASE / "assets/brand/logo.png",
                "intro": module.BASE / "assets/audio/intro.wav",
            },
        )

        assets = resolver()

        self.assertTrue(assets["brand"].is_file())
        self.assertTrue(assets["intro"].is_file())

    def test_image_model_can_be_routed_from_the_environment(self):
        """Catches a renderer that pins a retired model instead of using routing."""
        with mock.patch.dict(os.environ, {"AINTM_IMAGE_MODEL": "test-image-model"}):
            module = load_script_module()

        self.assertEqual("test-image-model", module.GEMINI_MODEL)


if __name__ == "__main__":
    unittest.main()
