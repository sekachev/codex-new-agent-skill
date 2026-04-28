#!/usr/bin/env python3
"""Smoke-test adaptive agent Codex hooks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".codex" / "hooks" / "dreaming.py"


def run(mode: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(HOOK), mode],
        input=json.dumps({"cwd": str(ROOT)}),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON from {mode}: {proc.stdout}") from exc


def main() -> int:
    session = run("session-start")
    if not session.get("continue"):
        raise SystemExit("session-start did not continue")
    if "hookSpecificOutput" not in session:
        raise SystemExit("session-start missing hookSpecificOutput")

    stop = run("stop")
    if not (stop.get("continue") or stop.get("decision") == "block"):
        raise SystemExit("stop hook returned unexpected payload")

    print("ok: session-start")
    print("ok: stop")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
