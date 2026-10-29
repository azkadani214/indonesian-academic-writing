"""Exercise packaging failures with isolated fixtures, not project wording."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_package.py"
SPEC = importlib.util.spec_from_file_location("validator", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills" / "sample-skill"
        self.skill.mkdir(parents=True)
        (self.root / "assets").mkdir()
        (self.root / "assets" / "logo.svg").write_text("<svg/>", encoding="utf-8")
        (self.root / "README.md").write_text("# Sample\n", encoding="utf-8")
        (self.root / "LICENSE").write_text("MIT\n", encoding="utf-8")
        (self.skill / "LICENSE").write_text("MIT\n", encoding="utf-8")
        self.entry = self.skill / "SKILL.md"
        self.entry.write_text(
            "---\nname: sample-skill\ndescription: Contoh pemeriksaan paket.\n"
            "license: MIT\n---\n# Contoh\n", encoding="utf-8")

    def append(self, text):
        with self.entry.open("a", encoding="utf-8") as file:
            file.write(text)

    def test_valid_package(self):
        self.assertEqual(VALIDATOR.validate(self.root), [])

    def test_missing_link(self):
        self.append("[Panduan](missing.md)\n")
        self.assertTrue(any("rusak" in e for e in VALIDATOR.validate(self.root)))

    def test_web_url_is_not_machine_path(self):
        self.append("[Sumber](https://example.org/source)\n")
        self.assertEqual(VALIDATOR.validate(self.root), [])

    def test_reference_outside_installable_folder(self):
        self.append("[README](../../README.md)\n")
        self.assertTrue(any("keluar" in e for e in VALIDATOR.validate(self.root)))

    def test_orphan_reference(self):
        (self.skill / "orphan.md").write_text("# Isi", encoding="utf-8")
        self.assertTrue(any("terjangkau" in e for e in VALIDATOR.validate(self.root)))

    def test_linked_reference(self):
        (self.skill / "guide.md").write_text("# Isi", encoding="utf-8")
        self.append("[Panduan](guide.md)\n")
        self.assertEqual(VALIDATOR.validate(self.root), [])

    def test_wrong_folder_name(self):
        text = self.entry.read_text(encoding="utf-8").replace("name: sample-skill", "name: other")
        self.entry.write_text(text, encoding="utf-8")
        self.assertTrue(any("Nama skill" in e for e in VALIDATOR.validate(self.root)))

    def test_machine_specific_path(self):
        self.append("Baca C:/private/file.txt\n")
        self.assertTrue(any("Path lokal" in e for e in VALIDATOR.validate(self.root)))

    def test_missing_bundled_license(self):
        (self.skill / "LICENSE").unlink()
        self.assertTrue(any("Lisensi" in e for e in VALIDATOR.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
