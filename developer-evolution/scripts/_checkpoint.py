"""Shared checkpoint persistence helpers for developer-evolution scripts."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, BinaryIO

if os.name == "nt":
    import msvcrt
else:
    import fcntl


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


def write_private_text(path: Path, content: str) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        path.parent.chmod(0o700)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False
        ) as handle:
            temporary = Path(handle.name)
            os.chmod(temporary, 0o600)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
        temporary = None
        if os.name != "nt":
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _acquire_lock(handle: BinaryIO) -> None:
    if os.name == "nt":
        handle.seek(0)
        if not handle.read(1):
            handle.write(b"\0")
            handle.flush()
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)


def _release_lock(handle: BinaryIO) -> None:
    if os.name == "nt":
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def checkpoint_lock(path: Path) -> Iterator[None]:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        path.parent.chmod(0o700)
    lock_path = path.with_name(f".{path.name}.lock")
    with lock_path.open("a+b") as handle:
        os.chmod(lock_path, 0o600)
        _acquire_lock(handle)
        try:
            yield
        finally:
            _release_lock(handle)


def write_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    """Atomically replace a checkpoint after validation."""
    if checkpoint.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        raise ValueError("Refusing to write an unsupported checkpoint schema")
    if not isinstance(checkpoint.get("sessions"), dict):
        raise ValueError("Refusing to write a checkpoint without a sessions object")

    content = json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n"
    write_private_text(path, content)
