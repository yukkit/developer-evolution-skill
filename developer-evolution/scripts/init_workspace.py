#!/usr/bin/env python3
"""Initialize developer-evolution state without overwriting user files."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

WORKSPACE_NAME = "developer-evolution"


HISTORY = """# Instruction History

Record approved and rejected developer-evolution proposals here. Keep evidence references concise and never include secrets or full transcripts.
"""

WATCHLIST = """# Preference Watchlist

Store uncertain observations awaiting evidence or confirmation. These are not runtime preferences.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the developer-evolution personalization workspace."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        help="Codex home directory. Defaults to CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help=(
            "Explicit workspace path. Defaults to "
            "<codex-home>/personalization/developer-evolution."
        ),
    )
    return parser.parse_args()


def resolve_codex_home(value: Path | None) -> Path:
    if value:
        return value.expanduser().resolve()
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def create_file(path: Path, content: str) -> str:
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        return "created"
    except FileExistsError:
        if os.name != "nt" and path.is_file():
            path.chmod(0o600)
        return "existing"


def ensure_private_directory(path: Path) -> None:
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        path.chmod(0o700)


def main() -> int:
    args = parse_args()
    codex_home = resolve_codex_home(args.codex_home)
    workspace = (
        args.workspace.expanduser().resolve()
        if args.workspace
        else codex_home / "personalization" / WORKSPACE_NAME
    )
    ensure_private_directory(workspace)
    ensure_private_directory(workspace / "evidence")
    ensure_private_directory(workspace / "proposals")

    results = {
        "workspace": str(workspace),
        "files": {
            "instruction-history.md": create_file(
                workspace / "instruction-history.md", HISTORY
            ),
            "watchlist.md": create_file(workspace / "watchlist.md", WATCHLIST),
        },
    }
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
