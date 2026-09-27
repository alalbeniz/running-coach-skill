#!/usr/bin/env python3
"""Build deterministic skill/plugin archives from the single root skill source.

Only maintainers need Python. The installed skill contains no executable code.
"""

import argparse
import json
import re
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


def chat_document():
    """Inline every coaching reference and resolve links within one attachment."""
    paths = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
    anchors = {p.resolve(): "coach-" + p.stem.lower() for p in paths}
    parts = ["""# Running Coach: contexto para esta conversación

Usa este documento como guía de coaching durante esta conversación, mientras esté
disponible en contexto, respetando las instrucciones posteriores del usuario.
Conector preferido: el complemento que seleccione el usuario; por ejemplo, @Garmin.
MissingMCP puede ser su proveedor, pero el complemento puede tener cualquier alias.
Este texto no instala herramientas, no habilita permisos ni garantiza memoria fuera
del chat. Si no tienes acceso al conector, trabaja con los datos que aporte el usuario.

Todas las referencias de coaching están incluidas abajo. Las indicaciones de leer
un archivo se refieren a la sección interna correspondiente: no necesitas acceder
a un repositorio, filesystem u otros adjuntos. Consulta solo el tema relevante.
Si solo recibes este documento, confirma brevemente que lo usarás sin iniciar
onboarding ni descargar datos. Si el usuario incluye una petición de coaching,
resuélvela directamente siguiendo estas instrucciones.

Versión autocontenida generada desde la skill y sus referencias. Contiene más texto
inicial que la skill modular; no promete la misma economía de contexto.
Licencia: GPL-3.0-only. Adaptación de running-coach-skill de Ivan Barcia.
"""]
    for path in paths:
        content = path.read_text(encoding="utf-8")
        if content.startswith("---\n"):
            content = content.split("---\n", 2)[2]

        def replace_link(match):
            label, target = match.groups()
            if "://" in target or target.startswith("#"):
                return match.group(0)
            resolved = (path.parent / target).resolve()
            if resolved not in anchors:
                raise ValueError(f"Reference cannot be inlined: {path.name} -> {target}")
            return f"[{label}](#{anchors[resolved]})"

        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, content)
        parts.append(f'<a id="{anchors[path.resolve()]}"></a>\n\n' + content.strip())
    return "\n\n---\n\n".join(parts).rstrip() + "\n"


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
    plugin["running-coach-chat.md"] = chat_document().encode("utf-8")
    plugin_zip = output / "running-coach-plugin.zip"
    write_archive(plugin_zip, manifest["name"], plugin)
    chat_md = output / "running-coach-chat.md"
    chat_md.write_text(chat_document(), encoding="utf-8")
    return skill_zip, plugin_zip, chat_md


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for result in build(args.output.resolve()):
        print(result)
