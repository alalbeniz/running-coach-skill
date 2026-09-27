#!/usr/bin/env python3
"""Build deterministic skill/plugin archives from the single root skill source.

Only maintainers need Python. The installed skill contains no executable code.
"""

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]


def skill_files():
    files = {"SKILL.md": (ROOT / "SKILL.md").read_bytes(),
             "LICENSE": (ROOT / "LICENSE").read_bytes()}
    for folder, suffix in (("references", ".md"), ("agents", ".yaml")):
        for path in sorted((ROOT / folder).rglob("*" + suffix)):
            if path.is_symlink():
                raise ValueError(f"Symlink not allowed in package: {path}")
            files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    return files


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def write_archive(path, prefix, files):
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            entry = ZipInfo(f"{prefix}/{name}", date_time=(2020, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "packaging/plugin.json").read_text())
    source = skill_files()
    skill_zip = output / "coach-skill.zip"
    write_archive(skill_zip, "coach", source)
    plugin = {f"skills/coach/{name}": data for name, data in source.items()}
    plugin["plugin.json"] = json_bytes(manifest)
    # Compatibility overlay is generated, never maintained separately.
    overlay = {key: manifest[key] for key in
               ("name", "version", "description", "author", "repository", "license")}
    overlay.update(manifest["extensions"]["com.openai"])
    overlay["skills"] = "./skills/"
    plugin[".codex-plugin/plugin.json"] = json_bytes(overlay)
    plugin["LICENSE"] = source["LICENSE"]
    plugin["README.md"] = (ROOT / "README.md").read_bytes()
    plugin_zip = output / "running-coach-plugin.zip"
    write_archive(plugin_zip, manifest["name"], plugin)
    return skill_zip, plugin_zip


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for result in build(args.output.resolve()):
        print(result)
