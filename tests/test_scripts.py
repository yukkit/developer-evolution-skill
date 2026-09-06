from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "developer-evolution"
COLLECTOR = SKILL_ROOT / "scripts" / "collect_history.py"
COMMITTER = SKILL_ROOT / "scripts" / "commit_checkpoint.py"
INITIALIZER = SKILL_ROOT / "scripts" / "init_workspace.py"


def workspace_path(codex_home: Path, *parts: str) -> Path:
    return codex_home / "personalization" / "developer-evolution" / Path(*parts)


def write_analysis_artifact(path: Path, bundle: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Analysis completed\n\nEvidence bundle: `{bundle.resolve()}`\n",
        encoding="utf-8",
    )


def write_session(path: Path, session_id: str, user_text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "timestamp": "2026-08-01T10:00:00Z",
                "cwd": "/workspace/example",
                "source": "cli",
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "id": "developer-1",
                "role": "developer",
                "content": [{"type": "input_text", "text": "SECRET=do-not-collect"}],
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "id": "user-1",
                "role": "user",
                "content": [{"type": "input_text", "text": user_text}],
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "id": "user-1",
                "role": "user",
                "content": [{"type": "input_text", "text": user_text}],
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "id": "assistant-1",
                "role": "assistant",
                "phase": "final_answer",
                "content": [{"type": "output_text", "text": "Understood."}],
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call_output",
                "output": "password=tool-secret-must-not-appear",
            },
        },
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def append_user_message(path: Path, item_id: str, text: str) -> None:
    row = {
        "type": "response_item",
        "payload": {
            "type": "message",
            "id": item_id,
            "role": "user",
            "content": [{"type": "input_text", "text": text}],
        },
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


class ScriptTests(unittest.TestCase):
    def test_workspace_initialization_is_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex"
            command = [
                sys.executable,
                str(INITIALIZER),
                "--codex-home",
                str(codex_home),
            ]
            first = json.loads(subprocess.check_output(command, text=True))
            profile = (
                codex_home
                / "personalization"
                / "developer-evolution"
                / "developer-profile.md"
            )
            profile.write_text("custom profile\n", encoding="utf-8")
            second = json.loads(subprocess.check_output(command, text=True))

            self.assertEqual(
                Path(first["workspace"]),
                codex_home / "personalization" / "developer-evolution",
            )
            self.assertEqual(first["files"]["developer-profile.md"], "created")
            self.assertEqual(second["files"]["developer-profile.md"], "existing")
            self.assertEqual(profile.read_text(encoding="utf-8"), "custom profile\n")
            if os.name != "nt":
                self.assertEqual(profile.stat().st_mode & 0o777, 0o600)
                self.assertEqual(Path(first["workspace"]).stat().st_mode & 0o777, 0o700)

    def test_collection_filters_redacts_deduplicates_and_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex"
            sessions = codex_home / "sessions" / "2026" / "08" / "01"
            included = sessions / "included.jsonl"
            active = sessions / "active.jsonl"
            old = sessions / "old.jsonl"

            user_text = (
                "<recommended_plugins>private host context</recommended_plugins>\n"
                "<skill>injected skill instructions</skill>\n"
                "# AGENTS.md instructions for /workspace/example\n"
                "<INSTRUCTIONS>injected project instructions</INSTRUCTIONS>\n"
                "I prefer explicit code. api_key=abcdef123456\n"
                "https://oss.example/object?OSSAccessKeyId=EXAMPLE123"
                "&Expires=1999999999&Signature=FAKE_SIGNATURE_VALUE\n"
                "https://example.test/download?token=FAKE_LONG_TOKEN_VALUE\n"
                "Authorization: Basic FAKE_AUTH_VALUE"
            )
            write_session(included, "session-included", user_text)
            write_session(active, "session-active", "active session")
            write_session(old, "session-old", "old session")

            now = datetime.now(tz=timezone.utc).timestamp()
            os.utime(included, (now - 3600, now - 3600))
            os.utime(active, (now, now))
            old_time = (datetime.now(tz=timezone.utc) - timedelta(days=40)).timestamp()
            os.utime(old, (old_time, old_time))

            output = workspace_path(codex_home, "evidence", "bundle.json")
            subprocess.run(
                [
                    sys.executable,
                    str(COLLECTOR),
                    "--codex-home",
                    str(codex_home),
                    "--days",
                    "30",
                    "--min-idle-minutes",
                    "15",
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            bundle = json.loads(output.read_text(encoding="utf-8"))

            self.assertEqual(bundle["summary"]["included_sessions"], 1)
            self.assertEqual(bundle["summary"]["active"], 1)
            self.assertEqual(bundle["summary"]["too_old"], 1)
            self.assertEqual(bundle["summary"]["redactions"]["credential"], 1)
            self.assertEqual(bundle["summary"]["redactions"]["url-query-credential"], 3)
            self.assertEqual(bundle["summary"]["redactions"]["header-credential"], 1)
            self.assertEqual(
                Path(bundle["checkpoint"]["path"]),
                codex_home
                / "personalization"
                / "developer-evolution"
                / "processing-state.json",
            )
            session = bundle["sessions"][0]
            self.assertEqual(session["session_id"], "session-included")
            self.assertEqual(session["message_count"], 2)
            collected = "\n".join(message["text"] for message in session["messages"])
            self.assertIn("I prefer explicit code", collected)
            self.assertIn("[REDACTED:credential]", collected)
            self.assertNotIn("private host context", collected)
            self.assertNotIn("injected skill instructions", collected)
            self.assertNotIn("injected project instructions", collected)
            self.assertNotIn("do-not-collect", collected)
            self.assertNotIn("tool-secret-must-not-appear", collected)
            self.assertNotIn("abcdef123456", collected)
            self.assertNotIn("FAKE_SIGNATURE_VALUE", collected)
            self.assertNotIn("FAKE_LONG_TOKEN_VALUE", collected)
            self.assertNotIn("FAKE_AUTH_VALUE", collected)
            if os.name != "nt":
                self.assertEqual(output.stat().st_mode & 0o777, 0o600)

    def test_markdown_user_only_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex"
            session = codex_home / "sessions" / "one.jsonl"
            write_session(session, "session-one", "Prefer small, reviewable changes.")
            old_enough = datetime.now(tz=timezone.utc).timestamp() - 3600
            os.utime(session, (old_enough, old_enough))

            result = subprocess.run(
                [
                    sys.executable,
                    str(COLLECTOR),
                    "--codex-home",
                    str(codex_home),
                    "--format",
                    "markdown",
                    "--user-only",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            output = Path(json.loads(result.stderr)["output"])
            content = output.read_text(encoding="utf-8")
            self.assertEqual(result.stdout, "")
            self.assertEqual(output.parent, workspace_path(codex_home, "evidence"))
            self.assertEqual(output.suffix, ".md")
            self.assertIn("Prefer small, reviewable changes.", content)
            self.assertNotIn("Understood.", content)

    def test_checkpoint_is_incremental_and_two_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            codex_home = root / "codex"
            session = codex_home / "sessions" / "one.jsonl"
            checkpoint = (
                codex_home
                / "personalization"
                / "developer-evolution"
                / "processing-state.json"
            )
            first_bundle = workspace_path(codex_home, "evidence", "first.json")
            proposal = workspace_path(codex_home, "proposals", "first.md")
            write_session(session, "session-one", "Prefer explicit code.")
            old_enough = datetime.now(tz=timezone.utc).timestamp() - 3600
            os.utime(session, (old_enough, old_enough))

            collect_command = [
                sys.executable,
                str(COLLECTOR),
                "--codex-home",
                str(codex_home),
                "--checkpoint",
                str(checkpoint),
                "--min-idle-minutes",
                "15",
            ]
            subprocess.run(
                [*collect_command, "--output", str(first_bundle)],
                check=True,
                capture_output=True,
                text=True,
            )
            first = json.loads(first_bundle.read_text(encoding="utf-8"))
            self.assertEqual(first["summary"]["included_sessions"], 1)
            self.assertEqual(first["summary"]["candidate_sessions"], 1)
            self.assertFalse(checkpoint.exists(), "collection must not advance state")

            write_analysis_artifact(proposal, first_bundle)
            subprocess.run(
                [
                    sys.executable,
                    str(COMMITTER),
                    "--bundle",
                    str(first_bundle),
                    "--checkpoint",
                    str(checkpoint),
                    "--proposal",
                    str(proposal),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            state = json.loads(checkpoint.read_text(encoding="utf-8"))
            self.assertIn("session-one", state["sessions"])
            repeated_commit = subprocess.run(
                [
                    sys.executable,
                    str(COMMITTER),
                    "--bundle",
                    str(first_bundle),
                    "--checkpoint",
                    str(checkpoint),
                    "--proposal",
                    str(proposal),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(json.loads(repeated_commit.stdout)["already_committed"])

            second_bundle = workspace_path(codex_home, "evidence", "second.json")
            subprocess.run(
                [*collect_command, "--output", str(second_bundle)],
                check=True,
                capture_output=True,
                text=True,
            )
            second = json.loads(second_bundle.read_text(encoding="utf-8"))
            self.assertEqual(second["summary"]["included_sessions"], 0)
            self.assertEqual(second["summary"]["unchanged_by_metadata"], 1)

            append_user_message(session, "user-2", "Avoid speculative abstractions.")
            os.utime(session, (old_enough + 60, old_enough + 60))
            changed_bundle = workspace_path(codex_home, "evidence", "changed.json")
            subprocess.run(
                [*collect_command, "--output", str(changed_bundle)],
                check=True,
                capture_output=True,
                text=True,
            )
            changed = json.loads(changed_bundle.read_text(encoding="utf-8"))
            self.assertEqual(changed["summary"]["included_sessions"], 1)

            repeated_bundle = workspace_path(codex_home, "evidence", "repeated.json")
            changed_proposal = workspace_path(codex_home, "proposals", "changed.md")
            write_analysis_artifact(changed_proposal, changed_bundle)
            subprocess.run(
                [*collect_command, "--output", str(repeated_bundle)],
                check=True,
                capture_output=True,
                text=True,
            )
            repeated = json.loads(repeated_bundle.read_text(encoding="utf-8"))
            self.assertEqual(
                repeated["summary"]["included_sessions"],
                1,
                "an uncommitted candidate must be processed again",
            )

            subprocess.run(
                [
                    sys.executable,
                    str(COMMITTER),
                    "--bundle",
                    str(changed_bundle),
                    "--checkpoint",
                    str(checkpoint),
                    "--proposal",
                    str(changed_proposal),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            final_bundle = workspace_path(codex_home, "evidence", "final.json")
            subprocess.run(
                [*collect_command, "--output", str(final_bundle)],
                check=True,
                capture_output=True,
                text=True,
            )
            final = json.loads(final_bundle.read_text(encoding="utf-8"))
            self.assertEqual(final["summary"]["included_sessions"], 0)
            self.assertEqual(final["summary"]["unchanged_by_metadata"], 1)

            os.utime(session, (old_enough + 120, old_enough + 120))
            metadata_bundle = workspace_path(
                codex_home, "evidence", "metadata-only.json"
            )
            subprocess.run(
                [*collect_command, "--output", str(metadata_bundle)],
                check=True,
                capture_output=True,
                text=True,
            )
            metadata_only = json.loads(metadata_bundle.read_text(encoding="utf-8"))
            self.assertEqual(metadata_only["summary"]["included_sessions"], 0)
            self.assertEqual(metadata_only["summary"]["candidate_sessions"], 1)
            self.assertEqual(metadata_only["summary"]["unchanged_by_content"], 1)
            metadata_proposal = workspace_path(
                codex_home, "proposals", "metadata-only.md"
            )
            write_analysis_artifact(metadata_proposal, metadata_bundle)
            subprocess.run(
                [
                    sys.executable,
                    str(COMMITTER),
                    "--bundle",
                    str(metadata_bundle),
                    "--checkpoint",
                    str(checkpoint),
                    "--proposal",
                    str(metadata_proposal),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_checkpoint_rejects_concurrent_state_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            codex_home = root / "codex"
            session = codex_home / "sessions" / "one.jsonl"
            checkpoint = (
                codex_home
                / "personalization"
                / "developer-evolution"
                / "processing-state.json"
            )
            bundle = workspace_path(codex_home, "evidence", "bundle.json")
            proposal = workspace_path(codex_home, "proposals", "proposal.md")
            write_session(session, "session-one", "Prefer boring technology.")
            old_enough = datetime.now(tz=timezone.utc).timestamp() - 3600
            os.utime(session, (old_enough, old_enough))
            subprocess.run(
                [
                    sys.executable,
                    str(COLLECTOR),
                    "--codex-home",
                    str(codex_home),
                    "--checkpoint",
                    str(checkpoint),
                    "--output",
                    str(bundle),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            write_analysis_artifact(proposal, bundle)

            checkpoint.parent.mkdir(parents=True, exist_ok=True)
            checkpoint.write_text(
                json.dumps({"schema_version": 1, "updated_at": None, "sessions": {}}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(COMMITTER),
                    "--bundle",
                    str(bundle),
                    "--checkpoint",
                    str(checkpoint),
                    "--proposal",
                    str(proposal),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("changed after collection", result.stderr)

    def test_collection_rejects_output_outside_private_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            codex_home = root / "codex"
            output = root / "bundle.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(COLLECTOR),
                    "--codex-home",
                    str(codex_home),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("Evidence output must be inside", result.stderr)
            self.assertFalse(output.exists())

    def test_collection_does_not_overwrite_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex"
            output = workspace_path(codex_home, "evidence", "bundle.json")
            command = [
                sys.executable,
                str(COLLECTOR),
                "--codex-home",
                str(codex_home),
                "--output",
                str(output),
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            original = output.read_bytes()
            repeated = subprocess.run(
                command, check=False, capture_output=True, text=True
            )
            self.assertEqual(repeated.returncode, 2)
            self.assertIn("Refusing to overwrite", repeated.stderr)
            self.assertEqual(output.read_bytes(), original)

    def test_malformed_session_is_not_checkpoint_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex"
            session = codex_home / "sessions" / "malformed.jsonl"
            output = workspace_path(codex_home, "evidence", "bundle.json")
            write_session(session, "session-malformed", "Prefer explicit code.")
            with session.open("a", encoding="utf-8") as handle:
                handle.write("{not valid json}\n")
            old_enough = datetime.now(tz=timezone.utc).timestamp() - 3600
            os.utime(session, (old_enough, old_enough))

            subprocess.run(
                [
                    sys.executable,
                    str(COLLECTOR),
                    "--codex-home",
                    str(codex_home),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            bundle = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(bundle["summary"]["parse_errors"], 1)
            self.assertEqual(bundle["summary"]["parse_error_sessions"], 1)
            self.assertEqual(bundle["summary"]["included_sessions"], 0)
            self.assertEqual(bundle["summary"]["candidate_sessions"], 0)

    def test_checkpoint_requires_artifact_bound_to_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex"
            session = codex_home / "sessions" / "one.jsonl"
            checkpoint = workspace_path(codex_home, "processing-state.json")
            bundle = workspace_path(codex_home, "evidence", "bundle.json")
            proposal = workspace_path(codex_home, "proposals", "proposal.md")
            write_session(session, "session-one", "Prefer explicit code.")
            old_enough = datetime.now(tz=timezone.utc).timestamp() - 3600
            os.utime(session, (old_enough, old_enough))
            subprocess.run(
                [
                    sys.executable,
                    str(COLLECTOR),
                    "--codex-home",
                    str(codex_home),
                    "--output",
                    str(bundle),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            proposal.parent.mkdir(parents=True, exist_ok=True)
            proposal.write_text("# Unrelated analysis\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(COMMITTER),
                    "--bundle",
                    str(bundle),
                    "--checkpoint",
                    str(checkpoint),
                    "--proposal",
                    str(proposal),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("exact evidence bundle path", result.stderr)
            self.assertFalse(checkpoint.exists())

    @unittest.skipIf(os.name == "nt", "fcntl assertion is POSIX-specific")
    def test_checkpoint_commit_waits_for_process_lock(self) -> None:
        import fcntl

        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex"
            session = codex_home / "sessions" / "one.jsonl"
            checkpoint = workspace_path(codex_home, "processing-state.json")
            bundle = workspace_path(codex_home, "evidence", "bundle.json")
            proposal = workspace_path(codex_home, "proposals", "proposal.md")
            write_session(session, "session-one", "Prefer explicit code.")
            old_enough = datetime.now(tz=timezone.utc).timestamp() - 3600
            os.utime(session, (old_enough, old_enough))
            subprocess.run(
                [
                    sys.executable,
                    str(COLLECTOR),
                    "--codex-home",
                    str(codex_home),
                    "--output",
                    str(bundle),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            write_analysis_artifact(proposal, bundle)
            checkpoint.parent.mkdir(parents=True, exist_ok=True)
            lock_path = checkpoint.with_name(f".{checkpoint.name}.lock")
            with lock_path.open("a+b") as lock_handle:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
                process = subprocess.Popen(
                    [
                        sys.executable,
                        str(COMMITTER),
                        "--bundle",
                        str(bundle),
                        "--checkpoint",
                        str(checkpoint),
                        "--proposal",
                        str(proposal),
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                time.sleep(0.2)
                self.assertIsNone(process.poll())
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
                _, stderr = process.communicate(timeout=5)
            self.assertEqual(process.returncode, 0, stderr)
            self.assertTrue(checkpoint.exists())


if __name__ == "__main__":
    unittest.main()
