#!/usr/bin/env python3
"""Deterministic Codex hook helper for adaptive agent memory.

This script does not call an LLM and does not summarize. It only tells Codex
which context to load and whether the Dreaming protocol from AGENTS.md is due.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def read_payload() -> dict[str, Any]:
    try:
        raw = sys.stdin.read().strip()
        return json.loads(raw) if raw else {}
    except Exception:
        return {}


def find_root(payload: dict[str, Any]) -> Path:
    cwd = payload.get("cwd") or os.getcwd()
    start = Path(cwd).expanduser().resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "AGENTS.md").exists() and (candidate / ".codex" / "hooks" / "dreaming.py").exists():
            return candidate
    return start


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def parse_date(text: str, key: str) -> dt.date | None:
    match = re.search(rf"^\s*{re.escape(key)}\s*:\s*([0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}|null)\s*$", text, re.M)
    if not match or match.group(1) == "null":
        return None
    try:
        return dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None


def parse_int(text: str, key: str, default: int) -> int:
    match = re.search(rf"^\s*{re.escape(key)}\s*:\s*(\d+)\s*$", text, re.M)
    if not match:
        return default
    try:
        return int(match.group(1))
    except ValueError:
        return default


def daily_logs(root: Path) -> list[tuple[dt.date, Path]]:
    logs_dir = root / "logs" / "daily"
    if not logs_dir.exists():
        return []
    out: list[tuple[dt.date, Path]] = []
    for path in logs_dir.glob("*.md"):
        match = DATE_RE.search(path.name)
        if not match:
            continue
        try:
            out.append((dt.date.fromisoformat(match.group(1)), path))
        except ValueError:
            continue
    return sorted(out, key=lambda item: item[0])


def onboarding_pending(root: Path) -> bool:
    text = read_text(root / "SOUL.md") + "\n" + read_text(root / "USER.md")
    return "onboarding_status: pending" in text or "onboarding_status: null" in text


def state(root: Path) -> dict[str, Any]:
    today = dt.date.today()
    memory = read_text(root / "MEMORY.md")
    last_dream = parse_date(memory, "last_dream")
    dream_after = parse_int(memory, "dream_after_new_logs", 3)
    logs = daily_logs(root)

    if last_dream:
        new_logs = [(day, path) for day, path in logs if day > last_dream]
    else:
        new_logs = logs

    reasons: list[str] = []
    if last_dream is None and len(logs) >= dream_after:
        reasons.append(f"no last_dream and {len(logs)} daily logs exist")
    if last_dream is not None and (today - last_dream).days >= 7:
        reasons.append(f"last_dream is {(today - last_dream).days} days old")
    if len(new_logs) >= dream_after:
        reasons.append(f"{len(new_logs)} new daily logs since last_dream")

    recent_days = {today, today - dt.timedelta(days=1)}
    recent = [path for day, path in logs if day in recent_days]

    return {
        "today": today.isoformat(),
        "last_dream": last_dream.isoformat() if last_dream else None,
        "recent_logs": [str(path.relative_to(root)) for path in recent],
        "log_count": len(logs),
        "new_log_count": len(new_logs),
        "due": bool(reasons),
        "reasons": reasons,
        "onboarding_pending": onboarding_pending(root),
    }


def emit(obj: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.stdout.flush()


def session_start(root: Path, st: dict[str, Any]) -> None:
    recent = ", ".join(st["recent_logs"]) if st["recent_logs"] else "none"
    due = "yes: " + "; ".join(st["reasons"]) if st["due"] else "no"
    pending = "yes" if st["onboarding_pending"] else "no"
    context = (
        "Adaptive Codex agent boot context:\n"
        "- Load AGENTS.md, SOUL.md, USER.md, and MEMORY.md.\n"
        f"- System date according to hook: {st['today']}.\n"
        f"- Load today's and yesterday's logs only: {recent}.\n"
        "- Do not auto-load older logs except for the current task, user request, contradiction, or dreaming.\n"
        f"- Onboarding pending: {pending}.\n"
        f"- Dreaming due: {due}.\n"
        "- If onboarding is pending, run $onboarding before normal work.\n"
        "- If dreaming is due, run the Dreaming protocol from AGENTS.md before normal work.\n"
        "- After meaningful turns, append a compact entry to logs/daily/YYYY-MM-DD.md.\n"
        "- If the user gives a durable preference/correction/fact, update USER.md or MEMORY.md immediately."
    )
    emit({
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        },
    })


def stop_hook(payload: dict[str, Any], st: dict[str, Any]) -> None:
    if payload.get("stop_hook_active"):
        emit({"continue": True})
        return
    if st["due"]:
        emit({
            "decision": "block",
            "reason": (
                "Before completing this turn, run the Dreaming protocol from AGENTS.md. "
                "Consolidate logs since last_dream into MEMORY.md and USER.md, update SOUL.md only with durable evidence, "
                "set last_dream to today's date, and leave raw logs intact. Reasons: "
                + "; ".join(st["reasons"])
            ),
        })
    else:
        emit({"continue": True})


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "session-start"
    try:
        payload = read_payload()
        root = find_root(payload)
        st = state(root)
        if mode == "stop":
            stop_hook(payload, st)
        else:
            session_start(root, st)
    except BaseException as exc:
        print(f"adaptive-agent hook failed open in {mode}: {exc}", file=sys.stderr)
        emit({"continue": True, "systemMessage": "Adaptive-agent hook failed open; continue normally."})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
