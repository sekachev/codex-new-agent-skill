#!/usr/bin/env python3
"""Create a Codex-native adaptive agent workspace from the bundled template."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Codex agent workspace.")
    parser.add_argument("target", help="Target directory for the new agent workspace.")
    parser.add_argument("--agent-name", default="Agent", help="Initial agent name.")
    parser.add_argument("--user-name", default="User", help="Initial user name.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files.")
    return parser.parse_args()


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def copy_template(template: Path, target: Path, values: dict[str, str], force: bool) -> list[Path]:
    written: list[Path] = []
    for src in sorted(template.rglob("*")):
        rel = src.relative_to(template)
        dest = target / rel
        if src.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue

        if dest.exists() and not force:
            raise SystemExit(f"Refusing to overwrite existing file: {dest}")

        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in {".md", ".toml", ".json", ".py", ".txt"} or src.name in {"AGENTS.md", "SOUL.md", "USER.md", "MEMORY.md"}:
            data = render(src.read_text(encoding="utf-8"), values)
            dest.write_text(data, encoding="utf-8")
        else:
            shutil.copy2(src, dest)
        written.append(dest)
    return written


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parents[1]
    template = skill_dir / "assets" / "agent-template"
    target = Path(args.target).expanduser().resolve()
    today = dt.date.today().isoformat()

    if not template.exists():
        raise SystemExit(f"Template not found: {template}")

    values = {
        "AGENT_NAME": args.agent_name.strip() or "Agent",
        "USER_NAME": args.user_name.strip() or "User",
        "TODAY": today,
    }

    target.mkdir(parents=True, exist_ok=True)
    written = copy_template(template, target, values, args.force)

    rels = [str(path.relative_to(target)) for path in written]
    print(f"Created Codex agent workspace at {target}")
    print(f"Wrote {len(rels)} files.")
    print("Next: open this folder in Codex and say: Begin onboarding")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
