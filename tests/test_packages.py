"""Check what a user actually installs, without Garmin access or extra libraries."""
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_packages", ROOT / "scripts/build_packages.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class PackagesTest(unittest.TestCase):
    def test_chat_document_is_self_contained_and_current(self):
        content = BUILDER.chat_document()
        anchors = re.findall(r'<a id="([^"]+)"></a>', content)
        self.assertEqual(len(anchors), len(set(anchors)))
        self.assertEqual(len(anchors), 1 + len(list((ROOT / "references").glob("*.md"))))
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if "://" not in link:
                self.assertTrue(link.startswith("#"), link)
                self.assertIn(link[1:], anchors)
        self.assertEqual(content, (ROOT / "docs/running-coach-chat.md").read_text())

    def test_installable_content_and_reproducibility(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            paths = BUILDER.build(output)
            first = [path.read_bytes() for path in paths]
            self.assertEqual(first, [path.read_bytes() for path in BUILDER.build(output)])
            with ZipFile(paths[0]) as skill, ZipFile(paths[1]) as plugin:
                self.assertIsNone(skill.testzip())
                self.assertIsNone(plugin.testzip())
                for name, source in BUILDER.skill_files().items():
                    self.assertEqual(source, skill.read("coach/" + name))
                    self.assertEqual(source, plugin.read("running-coach/skills/coach/" + name))
                self.assertEqual(sum(name.endswith("/SKILL.md") for name in plugin.namelist()), 1)
                portable = json.loads(plugin.read("running-coach/plugin.json"))
                legacy = json.loads(plugin.read("running-coach/.codex-plugin/plugin.json"))
                self.assertEqual(portable["name"], "running-coach")
                for field in ("name", "version", "description", "license"):
                    self.assertEqual(portable[field], legacy[field])
                self.assertEqual(portable["extensions"]["com.openai"]["interface"], legacy["interface"])
                self.assertEqual(legacy["skills"], "./skills/")
                self.assertTrue(any(name.startswith("running-coach/skills/coach/") for name in plugin.namelist()))
                for name in plugin.namelist():
                    self.assertNotIn("..", Path(name).parts)
                    self.assertNotIn(".git", Path(name).parts)

    def test_packaged_reference_links_resolve(self):
        files = BUILDER.skill_files()
        for name, data in files.items():
            if not name.endswith(".md"):
                continue
            for link in re.findall(r"\]\(([^)]+)\)", data.decode()):
                if "://" in link or link.startswith("#"):
                    continue
                target = (ROOT / name).parent / link.split("#")[0]
                relative = target.resolve().relative_to(ROOT).as_posix()
                self.assertTrue(relative in files, f"Broken packaged link: {name} -> {link}")


if __name__ == "__main__":
    unittest.main()
