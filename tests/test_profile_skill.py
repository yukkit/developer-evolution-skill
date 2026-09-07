from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CREATOR = (
    Path(__file__).resolve().parents[1]
    / "developer-evolution/scripts/create_profile_skill.py"
)


class ProfileSkillTests(unittest.TestCase):
    def create(
        self, codex_home: Path, profile: Path
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CREATOR),
                "--codex-home",
                str(codex_home),
                "--profile",
                str(profile),
            ],
            capture_output=True,
            text=True,
        )

    def test_creation_preserves_input_and_analysis_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            codex_home = root / "custom codex"
            codex_home.mkdir()
            profile = root / "approved.md"
            content = "# Developer Profile\n\n仅对示例项目：优先使用现有组件。\n"
            profile.write_text(content, encoding="utf-8")
            global_rules = codex_home / "AGENTS.md"
            global_rules.write_text("existing rules\n", encoding="utf-8")
            history = codex_home / "personalization/developer-evolution"
            history.mkdir(parents=True)
            rejected = history / "instruction-history.md"
            rejected.write_text("Rejected: forbidden preference\n", encoding="utf-8")
            watchlist = history / "watchlist.md"
            watchlist.write_text("Unconfirmed: maybe preference\n", encoding="utf-8")

            result = self.create(codex_home, profile)
            self.assertEqual(result.returncode, 0, result.stderr)
            skill = Path(json.loads(result.stdout)["skill"])
            self.assertEqual(skill, codex_home / "skills/developer-profile")
            self.assertEqual(profile.read_text(encoding="utf-8"), content)
            self.assertEqual(
                (skill / "references/profile.md").read_text(encoding="utf-8"), content
            )
            files = {
                p.relative_to(skill).as_posix() for p in skill.rglob("*") if p.is_file()
            }
            self.assertEqual(
                files, {"SKILL.md", "agents/openai.yaml", "references/profile.md"}
            )
            for path in skill.rglob("*"):
                if path.is_file():
                    body = path.read_text(encoding="utf-8")
                    self.assertNotIn("forbidden preference", body)
                    self.assertNotIn("maybe preference", body)
            self.assertNotIn(content, result.stdout + result.stderr)
            self.assertEqual(global_rules.read_text(), "existing rules\n")
            self.assertEqual(rejected.read_text(), "Rejected: forbidden preference\n")
            self.assertEqual(watchlist.read_text(), "Unconfirmed: maybe preference\n")
            self.assertFalse((history / "processing-state.json").exists())
            if os.name != "nt":
                for path in [skill, *skill.rglob("*")]:
                    self.assertEqual(
                        path.stat().st_mode & 0o777, 0o700 if path.is_dir() else 0o600
                    )

    def test_existing_personalized_skill_is_never_reset(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile = root / "approved.md"
            profile.write_text("# Approved\n", encoding="utf-8")
            codex_home = root / "codex"
            self.assertEqual(self.create(codex_home, profile).returncode, 0)
            skill = codex_home / "skills/developer-profile"
            (skill / "SKILL.md").write_text(
                "personalized entrypoint\n", encoding="utf-8"
            )
            (skill / "agents/openai.yaml").write_text(
                "custom invocation policy\n", encoding="utf-8"
            )
            before = {
                p.relative_to(skill): p.read_bytes()
                for p in skill.rglob("*")
                if p.is_file()
            }
            profile.write_text("# Newly approved\n", encoding="utf-8")

            result = self.create(codex_home, profile)
            self.assertEqual(result.returncode, 2)
            after = {
                p.relative_to(skill): p.read_bytes()
                for p in skill.rglob("*")
                if p.is_file()
            }
            self.assertEqual(after, before)

    def test_invalid_input_does_not_leave_an_installed_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile = root / "approved.md"
            codex_home = root / "codex"
            missing = self.create(codex_home, profile)
            self.assertEqual(missing.returncode, 2)
            profile.write_text(" \n", encoding="utf-8")
            empty = self.create(codex_home, profile)
            self.assertEqual(empty.returncode, 2)
            self.assertFalse((codex_home / "skills").exists())

    @unittest.skipIf(os.name == "nt", "POSIX symlink behavior")
    def test_refuses_existing_directory_file_and_dangling_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile = root / "approved.md"
            profile.write_text("# Approved\n", encoding="utf-8")
            for kind in ("directory", "file", "link"):
                with self.subTest(kind=kind):
                    codex_home = root / kind
                    target = codex_home / "skills/developer-profile"
                    target.parent.mkdir(parents=True)
                    if kind == "directory":
                        target.mkdir()
                    elif kind == "file":
                        target.write_text("keep me", encoding="utf-8")
                    else:
                        target.symlink_to(root / "missing")
                    result = self.create(codex_home, profile)
                    self.assertEqual(result.returncode, 2)
                    if kind == "directory":
                        self.assertEqual(list(target.iterdir()), [])
                    elif kind == "file":
                        self.assertEqual(target.read_text(), "keep me")
                    else:
                        self.assertTrue(target.is_symlink())


if __name__ == "__main__":
    unittest.main()
