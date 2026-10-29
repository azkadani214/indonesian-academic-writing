"""Validate this repository's simple skill metadata and portable local links.

Standard library only. This is not a general YAML or Markdown parser and does
not verify external URLs, citation truth, or agent behavior.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")
HTML_SRC = re.compile(r'<img\b[^>]*\bsrc=[\"\']([^\"\']+)[\"\']', re.I)
ABSOLUTE = re.compile(r"(?:(?<![A-Za-z0-9])[A-Za-z]:[\\/]|file://|/Users/|/home/|/mnt/)")


def local_targets(text: str):
    for raw in [*LINK.findall(text), *HTML_SRC.findall(text)]:
        target = raw.strip().strip("<>")
        if target.startswith("#") or urlsplit(target).scheme:
            continue
        yield unquote(target.split("#", 1)[0])


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    skill_dirs = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_dirs:
        return ["Tidak ada skills/<nama>/SKILL.md."]

    for required in ("README.md", "LICENSE", "assets/logo.svg"):
        if not (root / required).is_file():
            errors.append(f"Berkas wajib hilang: {required}")

    for entry in skill_dirs:
        skill_root = entry.parent.resolve()
        content = entry.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
        if not match:
            errors.append(f"Frontmatter tidak ditemukan: {entry.relative_to(root)}")
            continue
        header = match.group(1)
        values = {}
        for key in ("name", "description", "license"):
            matches = re.findall(rf"^{key}:\s*(.+)$", header, re.M)
            if len(matches) != 1:
                errors.append(f"Metadata {key} harus muncul tepat sekali: {entry}")
                continue
            value = matches[0].strip().strip('\"\'')
            if not value or value in ("|", ">", "null", "~"):
                errors.append(f"Metadata {key} harus berupa teks satu baris: {entry}")
            values[key] = value
        name = values.get("name", "")
        if (not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
                or len(name) > 64 or name != skill_root.name):
            errors.append(f"Nama skill tidak valid/tidak sesuai direktori: {name}")
        if len(values.get("description", "")) > 1024:
            errors.append(f"Deskripsi melebihi 1024 karakter: {name}")
        if not (skill_root / "LICENSE").is_file():
            errors.append(f"Lisensi tidak ikut paket: {name}")
        graph: dict[Path, set[Path]] = {}
        for file in skill_root.rglob("*.md"):
            text = file.read_text(encoding="utf-8")
            if ABSOLUTE.search(text):
                errors.append(f"Path lokal mesin ditemukan: {file.relative_to(root)}")
            if "[TODO:" in text or "\ufffd" in text:
                errors.append(f"Scaffold/karakter rusak: {file.relative_to(root)}")
            graph[file.resolve()] = set()
            for target in local_targets(text):
                dest = (file.parent / target).resolve()
                if not dest.is_relative_to(skill_root):
                    errors.append(f"Tautan keluar dari paket: {file.relative_to(root)} -> {target}")
                if dest.is_file() and dest.suffix == ".md":
                    graph[file.resolve()].add(dest)
        seen, pending = set(), [entry.resolve()]
        while pending:
            item = pending.pop()
            if item in seen:
                continue
            seen.add(item)
            pending.extend(graph.get(item, set()) - seen)
        for file in graph.keys() - seen:
            errors.append(f"Referensi tidak terjangkau dari SKILL.md: {file.relative_to(root)}")

    for base in (root, root / "docs", root / "tests", root / "skills"):
        files = base.glob("*.md") if base == root else base.rglob("*.md")
        for file in files:
            text = file.read_text(encoding="utf-8")
            for target in local_targets(text):
                dest = (file.parent / target).resolve()
                if not dest.is_relative_to(root) or not dest.exists():
                    errors.append(f"Tautan lokal rusak: {file.relative_to(root)} -> {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("LULUS: metadata sederhana, struktur, lisensi, tautan lokal, dan portabilitas paket.")
    print("Tidak mencakup verifikasi URL eksternal, fakta, atau perilaku agen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
