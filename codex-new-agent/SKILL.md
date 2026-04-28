---
name: codex-new-agent
description: Create a new adaptive Codex-native agent workspace from a reusable template. Use when the user asks to create, scaffold, initialize, bootstrap, or install a personal/project agent with onboarding, durable memory, daily logs, Codex hooks, and dreaming-style memory consolidation.
---

# Codex New Agent

Use this skill to scaffold a Codex-native agent that lives in a workspace, adapts to its user, and preserves continuity through files rather than background services.

The generated agent is intentionally not an always-on OpenClaw/Hermes clone. It has no heartbeat, no daemon, no squad/subagent roster, and no `ACTIVE.md`. Codex wakes it through normal sessions and project hooks.

## Create The Agent

Run the bundled script from the skill directory:

```bash
python3 scripts/create_agent.py /absolute/path/to/new-agent \
  --agent-name "Agent" \
  --user-name "User"
```

Add `--force` only when the user explicitly wants to overwrite an existing incomplete scaffold. The script copies `assets/agent-template/`, replaces placeholders, and refuses to overwrite existing files by default.

After scaffolding, tell the user to open the generated folder in Codex and start with:

```text
Begin onboarding
```

## Generated Structure

The scaffold creates:

```text
AGENTS.md
SOUL.md
USER.md
MEMORY.md
logs/daily/.gitkeep
.agents/skills/onboarding/SKILL.md
.codex/config.toml
.codex/hooks.json
.codex/hooks/dreaming.py
.codex/hooks/smoke_test.py
```

## Operating Model

- Load `SOUL.md`, `USER.md`, `MEMORY.md`, and today's/yesterday's daily logs at boot.
- Append a compact entry to `logs/daily/YYYY-MM-DD.md` after each meaningful turn.
- If the user says something durable, important, corrective, or preference-like, write it immediately to `MEMORY.md` or `USER.md`; do not wait for dreaming.
- Use `SOUL.md` for durable changes to agent character, helpfulness model, tone, initiative, and adaptation settings.
- Use `MEMORY.md` for long-term lessons, user-specific workflows, environment facts, and dreaming state.
- Use daily logs as raw capture only. Do not treat them as future behavior configuration.
- Trigger dreaming through Codex hooks or explicit user request. Dreaming consolidates recent logs, prunes noise, and updates `MEMORY.md`, `USER.md`, and `SOUL.md` when there is durable evidence.

## Adaptive Usefulness

The generated agent's core mission is to be useful to the specific user. "Useful" is not predefined. The agent must form and revise a working hypothesis:

- what outcomes the user values;
- how much autonomy they want;
- which tone, depth, and pace help them;
- which repeated corrections should become durable memory;
- which workflows deserve a new skill.

When a reusable workflow deserves a new skill, use Codex's native `CreateSkill` capability. Do not invent a separate skill-creation mechanism inside the generated agent.

## Safety Model

Do not require confirmation for ordinary helpful work. Require explicit confirmation for destructive, irreversible, external, or high-risk actions, including deletion, overwriting critical config, sending messages, publishing, payments, credential changes, and mass edits.

Never store secrets, tokens, passwords, or private credentials in `MEMORY.md`, `USER.md`, `SOUL.md`, or daily logs. Keep secrets in local ignored environment files.

## References

For design rationale and source ideas, read `references/design-notes.md` only when you need to modify the scaffold or explain why it works.
