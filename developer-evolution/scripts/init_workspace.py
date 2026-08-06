#!/usr/bin/env python3
"""Initialize developer-evolution state without overwriting user files."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


WORKSPACE_NAME = "developer-evolution"


PROFILE = """# Developer Profile

This file contains evidence-backed observations about the developer. It is not automatically loaded as an instruction file.

## Technical preferences

## Coding philosophy

## Decision patterns

## Code style

## AI collaboration style

## Recurring frustrations

## Communication style

## Inconsistencies and changes
"""

HISTORY = """# Instruction History

Append approved developer-evolution changes here. Keep evidence references concise and never include secrets or full transcripts.
"""

WATCHLIST = """# Preference Watchlist

Store plausible patterns that do not yet meet the evidence threshold for active instructions.
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
        with path.open("x", encoding="utf-8") as handle:
            handle.write(content)
        return "created"
    except FileExistsError:
        return "existing"


def main() -> int:
    args = parse_args()
    codex_home = resolve_codex_home(args.codex_home)
    workspace = (
        args.workspace.expanduser().resolve()
        if args.workspace
        else codex_home / "personalization" / WORKSPACE_NAME
    )
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "evidence").mkdir(exist_ok=True)
    (workspace / "proposals").mkdir(exist_ok=True)

    results = {
        "workspace": str(workspace),
        "files": {
            "developer-profile.md": create_file(workspace / "developer-profile.md", PROFILE),
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
