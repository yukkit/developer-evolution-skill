"""Shared checkpoint persistence helpers for developer-evolution scripts."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any


CHECKPOINT_SCHEMA_VERSION = 1


def empty_checkpoint() -> dict[str, Any]:
    return {
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
        "updated_at": None,
        "sessions": {},
    }


def load_checkpoint(path: Path) -> tuple[dict[str, Any], str | None]:
    """Load and validate a checkpoint, returning its exact file digest."""
    if not path.exists():
        return empty_checkpoint(), None
    if not path.is_file():
        raise ValueError(f"Checkpoint is not a file: {path}")

    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    try:
        checkpoint = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Checkpoint is not valid JSON: {path}: {error}") from error

    if not isinstance(checkpoint, dict):
        raise ValueError(f"Checkpoint root must be an object: {path}")
    if checkpoint.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported checkpoint schema_version in {path}: "
            f"{checkpoint.get('schema_version')!r}"
        )
    if not isinstance(checkpoint.get("sessions"), dict):
        raise ValueError(f"Checkpoint sessions must be an object: {path}")
    for session_id, entry in checkpoint["sessions"].items():
        if not isinstance(session_id, str) or not isinstance(entry, dict):
            raise ValueError(f"Invalid checkpoint session entry in {path}")
    return checkpoint, digest


def write_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    """Atomically replace a checkpoint after validation."""
    if checkpoint.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        raise ValueError("Refusing to write an unsupported checkpoint schema")
    if not isinstance(checkpoint.get("sessions"), dict):
        raise ValueError("Refusing to write a checkpoint without a sessions object")

    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    temporary.replace(path)

