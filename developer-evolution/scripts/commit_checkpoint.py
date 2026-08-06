#!/usr/bin/env python3
"""Commit a collector checkpoint candidate after analysis succeeds."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _checkpoint import CHECKPOINT_SCHEMA_VERSION, load_checkpoint, write_checkpoint


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Atomically commit checkpoint candidates from a JSON evidence bundle."
    )
    parser.add_argument("--bundle", required=True, type=Path, help="JSON evidence bundle.")
    parser.add_argument(
        "--checkpoint",
        type=Path,
        help="Checkpoint path. Must match the path recorded in the bundle.",
    )
    parser.add_argument(
        "--proposal",
        type=Path,
        help="Optional proposal or no-change report proving analysis completed.",
    )
    return parser.parse_args()


def load_bundle(path: Path) -> dict[str, Any]:
    try:
        bundle = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read JSON evidence bundle {path}: {error}") from error
    if not isinstance(bundle, dict):
        raise ValueError("Evidence bundle root must be an object")
    if bundle.get("source") != "local-codex-sessions":
        raise ValueError("Evidence bundle has an unsupported source")
    checkpoint = bundle.get("checkpoint")
    if not isinstance(checkpoint, dict):
        raise ValueError("Evidence bundle has no checkpoint candidate")
    if checkpoint.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        raise ValueError("Evidence bundle has an unsupported checkpoint schema")
    if not isinstance(checkpoint.get("candidate_sessions"), dict):
        raise ValueError("Evidence bundle checkpoint candidate is malformed")
    return bundle


def resolve_target(args: argparse.Namespace, bundle: dict[str, Any]) -> Path:
    recorded = bundle["checkpoint"].get("path")
    if not isinstance(recorded, str) or not recorded:
        raise ValueError("Evidence bundle does not record a checkpoint path")
    recorded_path = Path(recorded).expanduser().resolve()
    if args.checkpoint is None:
        return recorded_path
    requested = args.checkpoint.expanduser().resolve()
    if requested != recorded_path:
        raise ValueError(
            f"Requested checkpoint does not match bundle: {requested} != {recorded_path}"
        )
    return requested


def validate_candidates(candidates: dict[str, Any]) -> None:
    for session_id, entry in candidates.items():
        if not isinstance(session_id, str) or not isinstance(entry, dict):
            raise ValueError("Malformed checkpoint session candidate")
        if entry.get("session_id") != session_id:
            raise ValueError(f"Checkpoint candidate ID mismatch: {session_id}")


def already_committed(
    current: dict[str, Any],
    candidates: dict[str, Any],
    bundle_path: Path,
    proposal_path: Path | None,
) -> bool:
    if not candidates:
        return True
    comparable_fields = {
        "session_id",
        "source_file",
        "file_size",
        "modified_at_ns",
        "modified_at",
        "session_fingerprint",
        "extraction_signature",
    }
    for session_id, candidate in candidates.items():
        committed = current["sessions"].get(session_id)
        if not isinstance(committed, dict):
            return False
        if any(committed.get(field) != candidate.get(field) for field in comparable_fields):
            return False
        if committed.get("evidence_bundle") != str(bundle_path):
            return False
        if proposal_path is not None and committed.get("proposal") != str(proposal_path):
            return False
    return True


def main() -> int:
    args = parse_args()
    bundle_path = args.bundle.expanduser().resolve()
    try:
        bundle = load_bundle(bundle_path)
        checkpoint_path = resolve_target(args, bundle)
        if args.proposal is not None:
            proposal_path = args.proposal.expanduser().resolve()
            if not proposal_path.is_file():
                raise ValueError(f"Proposal or report does not exist: {proposal_path}")
        else:
            proposal_path = None

        candidates = bundle["checkpoint"]["candidate_sessions"]
        validate_candidates(candidates)
        current, current_digest = load_checkpoint(checkpoint_path)
        expected_digest = bundle["checkpoint"].get("base_digest")
        if current_digest != expected_digest:
            if already_committed(current, candidates, bundle_path, proposal_path):
                print(
                    json.dumps(
                        {
                            "checkpoint": str(checkpoint_path),
                            "updated": False,
                            "already_committed": True,
                            "committed_sessions": len(candidates),
                        }
                    )
                )
                return 0
            raise ValueError(
                "Checkpoint changed after collection; rerun collection before committing"
            )

        if not candidates:
            print(
                json.dumps(
                    {
                        "checkpoint": str(checkpoint_path),
                        "updated": False,
                        "committed_sessions": 0,
                    }
                )
            )
            return 0

        sessions = dict(current["sessions"])
        committed_at = datetime.now(tz=timezone.utc).isoformat()
        for session_id, entry in candidates.items():
            committed = dict(entry)
            committed["processed_at"] = committed_at
            committed["evidence_bundle"] = str(bundle_path)
            if proposal_path is not None:
                committed["proposal"] = str(proposal_path)
            sessions[session_id] = committed

        updated = {
            "schema_version": CHECKPOINT_SCHEMA_VERSION,
            "updated_at": committed_at,
            "last_evidence_bundle": str(bundle_path),
            "last_proposal": str(proposal_path) if proposal_path else None,
            "sessions": sessions,
        }
        write_checkpoint(checkpoint_path, updated)
        print(
            json.dumps(
                {
                    "checkpoint": str(checkpoint_path),
                    "updated": True,
                    "committed_sessions": len(candidates),
                    "total_sessions": len(sessions),
                }
            )
        )
        return 0
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
