#!/usr/bin/env python3
"""Create a private runtime skill from a reviewed profile without overwriting one."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

from init_workspace import create_file, ensure_private_directory, resolve_codex_home


def create_profile_skill(codex_home: Path, profile: Path) -> Path:
    skills = codex_home / "skills"
    target = skills / "developer-profile"
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Refusing to overwrite existing skill: {target}")

    content = profile.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError("Reviewed profile is empty")
    assets = Path(__file__).resolve().parents[1] / "assets"
    files = {
        "SKILL.md": (assets / "profile-skill.md").read_text(encoding="utf-8"),
        "agents/openai.yaml": (assets / "profile-openai.yaml").read_text(
            encoding="utf-8"
        ),
        "references/profile.md": content,
    }

    skills.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".developer-profile-", dir=skills) as temp:
        staged = Path(temp) / "developer-profile"
        ensure_private_directory(staged)
        for name, text in files.items():
            path = staged / name
            ensure_private_directory(path.parent)
            create_file(path, text)
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Refusing to overwrite existing skill: {target}")
        os.rename(staged, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create developer-profile after authorization to activate it."
    )
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument(
        "--profile",
        type=Path,
        required=True,
        help="Reviewed Markdown containing only preferences authorized for runtime use.",
    )
    args = parser.parse_args()
    try:
        target = create_profile_skill(
            resolve_codex_home(args.codex_home), args.profile.expanduser().resolve()
        )
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")
    print(json.dumps({"skill": str(target), "created": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
