import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "rank_and_script.py"


def load_script_module():
    spec = importlib.util.spec_from_file_location("rank_and_script", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RankAndScriptTest(unittest.TestCase):
    def test_daily_writer_uses_grok_and_emits_first_presenter_asset_path(self):
        """Catches a Claude regression and presenter IDs that lose their asset path."""
        module = load_script_module()

        with tempfile.TemporaryDirectory() as raw_tmp:
            tmp = Path(raw_tmp)
            characters = tmp / "characters.yml"
            rotation = tmp / "rotation.json"
            candidates = tmp / "candidates.json"
            episode = tmp / "episode.json"
            fake_bin = tmp / "bin"
            fake_bin.mkdir()

            characters.write_text(
                "girl1:\n"
                "  name: Siobhan\n"
                "  voice: en-GB-SoniaNeural\n"
                "  personality: Cool and incisive.\n"
                "  images: assets/characters/girl3-Siobhan\n"
                "girl2:\n"
                "  name: Gemma\n"
                "  voice: en-US-JennyNeural\n"
                "  personality: Smart and dryly funny.\n"
                "  images: assets/characters/girl2-Gemma\n"
                "girl3:\n"
                "  name: Claudia\n"
                "  voice: en-US-AvaNeural\n"
                "  personality: Calm and enthusiastic.\n"
                "  images: assets/characters/girl1-Claudia\n"
            )
            candidates.write_text(
                json.dumps(
                    {
                        "stories": [
                            {
                                "id": "story-1",
                                "title": "Verified AI release",
                                "url": "https://example.com/release",
                                "source": "Primary source",
                                "summary": "A verified release summary.",
                            }
                        ]
                    }
                )
            )

            fake_grok = fake_bin / "grok"
            fake_grok.write_text(
                "#!/usr/bin/python3\n"
                "import json, sys\n"
                "required = {'--model', 'grok-4.6', '--reasoning-effort', 'medium'}\n"
                "if not required.issubset(set(sys.argv[1:])):\n"
                "    raise SystemExit('missing required model routing arguments')\n"
                "print(json.dumps({\n"
                "  'chosen_story': {'id': 'story-1', 'title': 'Verified AI release', "
                "'url': 'https://example.com/release', 'source': 'Primary source'},\n"
                "  'runner_up': None,\n"
                "  'headline': 'A Verified AI Release',\n"
                "  'script': 'This is a verified test script for the daily lead video.',\n"
                "  'captions': {'tiktok': '', 'instagram': '', 'youtube': '', 'x_thread': []},\n"
                "  'image_prompts': ['A vertical editorial AI scene'],\n"
                "  'provider_marker': 'grok'\n"
                "}))\n"
            )
            fake_grok.chmod(0o755)

            fake_claude = fake_bin / "claude"
            fake_claude.write_text(
                "#!/usr/bin/python3\n"
                "import json\n"
                "print(json.dumps({\n"
                "  'chosen_story': {'id': 'story-1', 'title': 'Verified AI release', "
                "'url': 'https://example.com/release', 'source': 'Primary source'},\n"
                "  'runner_up': None,\n"
                "  'headline': 'A Verified AI Release',\n"
                "  'script': 'This is a verified test script for the daily lead video.',\n"
                "  'captions': {'tiktok': '', 'instagram': '', 'youtube': '', 'x_thread': []},\n"
                "  'image_prompts': ['A vertical editorial AI scene'],\n"
                "  'provider_marker': 'claude'\n"
                "}))\n"
            )
            fake_claude.chmod(0o755)

            module.CHARS = characters
            module.ROTATION = rotation
            argv = [
                str(SCRIPT),
                "--candidates",
                str(candidates),
                "--out",
                str(episode),
            ]
            with mock.patch.object(sys, "argv", argv), mock.patch.dict(
                os.environ, {"PATH": str(fake_bin)}
            ):
                module.main()

            result = json.loads(episode.read_text())
            self.assertEqual("grok", result.get("provider_marker"))
            self.assertEqual("girl1", result.get("presenter_id"))
            self.assertEqual("Siobhan", result.get("presenter_name"))
            self.assertEqual(
                "assets/characters/girl3-Siobhan", result.get("presenter_images")
            )


if __name__ == "__main__":
    unittest.main()
