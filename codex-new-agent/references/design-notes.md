# Design Notes

This skill combines three patterns:

1. OpenClaw-style workspace identity: `SOUL.md`, `USER.md`, `MEMORY.md`, daily logs, and strong "write it down" discipline.
2. Hermes-style adaptive learning loop: remember user preferences and corrections, keep memory bounded, and turn repeated workflows into skills.
3. Codex-native hooks: use `SessionStart` and `Stop` hooks as deterministic reminders, not as background agents.

## Memory Rules

Use daily logs for raw capture and `MEMORY.md` / `USER.md` for durable facts.

Promote immediately when the user says:

- "remember this";
- "always" / "never";
- a correction about the agent's behavior;
- a stable preference;
- a personal or project fact that prevents repetition later.

Keep memory declarative:

- Good: "User prefers concise status updates during long tasks."
- Risky: "Always be concise."

Imperatives in memory can become accidental system instructions. Put procedures in skills, not memory.

## Dreaming

Dreaming is consolidation, not logging. It should:

- read `MEMORY.md`, `USER.md`, `SOUL.md`, and logs after `last_dream`;
- identify durable patterns, preferences, corrections, workflows, and noise;
- update long-term files compactly;
- leave raw logs intact;
- update `last_dream`.

## Why No ACTIVE.md

Codex already has the live conversation and the generated agent appends compact daily logs after meaningful turns. A separate active-task file adds one more place to forget or duplicate state. If a future user genuinely needs task checkpointing, create a skill or project-specific file after the pattern appears.

## Why No Heartbeat

Codex skills do not run autonomous background work. The generated agent relies on project hooks and explicit turns. This keeps the scaffold portable, inspectable, and safe.
