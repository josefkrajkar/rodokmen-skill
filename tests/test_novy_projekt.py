"""Regrese založení a aktualizace projektu; jen standardní knihovna Pythonu."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1] / "skills" / "rodokmen"
GENERATOR = SKILL / "tools" / "novy_projekt.py"


def snapshot(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*") if p.is_file()
    }


class ProjectGenerationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Rodokmen Novákových"

    def generate(self, *args):
        return subprocess.run(
            [sys.executable, "-I", str(GENERATOR), str(self.project), *args],
            cwd=self.temp.name, capture_output=True, text=True, encoding="utf-8", check=True,
        )

    def test_new_project_has_both_clients_and_shared_instructions(self):
        self.generate()
        for name in ("AGENTS.md", "CLAUDE.md", ".claude/launch.json", "data/STAV.md", "tools/kontrola.py", "web/package.json"):
            self.assertTrue((self.project / name).is_file(), name)
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), (SKILL / "template/AGENTS.md").read_bytes())
        self.assertEqual((self.project / ".skill_verze").read_bytes(), (SKILL / "VERZE").read_bytes())

    def test_repeat_generation_preserves_all_file_contents(self):
        self.generate("--ukazka")
        before = snapshot(self.project)
        self.generate("--ukazka")
        self.assertEqual(snapshot(self.project), before)
        self.assertEqual(list((self.project / "pracovni").glob("zaloha_web_*")), [])

    def test_upgrade_adds_codex_instructions_and_preserves_family_data(self):
        self.generate("--ukazka")
        (self.project / "AGENTS.md").unlink()  # projekt před podporou Codexu
        (self.project / "CLAUDE.md").write_text("Vlastní pravidla rodiny.\n", encoding="utf-8")
        (self.project / "data/STAV.md").write_text("Rozpracováno: hledáme v Třeboni.\n", encoding="utf-8")
        (self.project / ".skill_verze").write_text("0.5.0\n", encoding="utf-8")
        before_data = snapshot(self.project / "data")
        self.generate()
        self.assertTrue((self.project / "AGENTS.md").is_file())
        self.assertEqual(snapshot(self.project / "data"), before_data)
        self.assertEqual((self.project / "CLAUDE.md").read_text(encoding="utf-8"), "Vlastní pravidla rodiny.\n")
        self.assertEqual((self.project / ".skill_verze").read_bytes(), (SKILL / "VERZE").read_bytes())

    def test_preserves_existing_instructions_and_preview_settings(self):
        self.generate()
        names = ("AGENTS.md", "CLAUDE.md", ".claude/launch.json", "poznamky_pro_skill.md")
        for name in names:
            (self.project / name).write_text("Vlastní obsah: " + name, encoding="utf-8")
        self.generate()
        for name in names:
            self.assertEqual((self.project / name).read_text(encoding="utf-8"), "Vlastní obsah: " + name)

    def test_web_update_backs_up_customizations_and_refreshes_tools(self):
        self.generate("--ukazka")
        style = self.project / "web/src/styles/global.css"
        style.write_text("/* Vlastní vzhled */\n", encoding="utf-8")
        (self.project / "tools/kontrola.py").write_text("# starší nástroj\n", encoding="utf-8")
        before_data = snapshot(self.project / "data")
        self.generate()
        backups = list((self.project / "pracovni").glob("zaloha_web_*/src/styles/global.css"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "/* Vlastní vzhled */\n")
        self.assertEqual(style.read_bytes(), (SKILL / "template/web/src/styles/global.css").read_bytes())
        self.assertEqual((self.project / "tools/kontrola.py").read_bytes(), (SKILL / "tools/kontrola.py").read_bytes())
        self.assertEqual(snapshot(self.project / "data"), before_data)

    def test_demo_data_passes_consistency_check(self):
        self.generate("--ukazka")
        result = subprocess.run(
            [sys.executable, "-I", str(self.project / "tools/kontrola.py")],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
