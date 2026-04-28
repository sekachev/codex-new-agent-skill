# Codex New Agent Skill

Create adaptive Codex-native agents with durable memory, onboarding, daily logs, and dreaming-style consolidation.

This skill scaffolds a workspace agent that lives entirely inside a Codex project. It borrows the best parts of OpenClaw and Hermes-style agents, but removes always-on background behavior: no heartbeat, no daemon, no subagent roster, no `ACTIVE.md`.

## What It Creates

```text
AGENTS.md
SOUL.md
USER.md
MEMORY.md
logs/daily/
.agents/skills/onboarding/SKILL.md
.codex/config.toml
.codex/hooks.json
.codex/hooks/dreaming.py
```

The generated agent:

- loads `SOUL.md`, `USER.md`, `MEMORY.md`, and today's/yesterday's logs on boot;
- writes compact daily logs after meaningful turns;
- immediately saves durable user preferences and corrections to long-term memory;
- uses Codex hooks to detect when dreaming is due;
- adapts its helpfulness model over time;
- asks confirmation only for destructive, irreversible, external, or high-risk actions;
- uses Codex native `CreateSkill` when repeated workflows deserve a skill.

## Install

In Codex, ask:

```text
Install this skill:
https://github.com/sekachev/codex-new-agent-skill/tree/main/codex-new-agent
```

Or install with the bundled skill installer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/sekachev/codex-new-agent-skill/tree/main/codex-new-agent
```

Restart Codex after installing.

## Use

Ask Codex:

```text
Use codex-new-agent to create a new agent in /path/to/my-agent called Atlas for Nikolai.
```

The skill runs:

```bash
python3 scripts/create_agent.py /path/to/my-agent --agent-name Atlas --user-name Nikolai
```

Then open the generated folder in Codex and say:

```text
Begin onboarding
```

## Pinned Repo Card

Suggested GitHub profile pinned-card text:

**Codex New Agent Skill**  
Scaffold adaptive Codex-native agents with SOUL.md, USER.md, MEMORY.md, daily logs, onboarding, hooks, and dreaming-style memory consolidation.

Suggested repo description:

```text
Create adaptive Codex-native agents with memory, onboarding, hooks, and dreaming.
```

Suggested topics:

```text
codex, codex-skill, ai-agent, memory, onboarding, openclaw, hermes-agent, agent-skills
```

## License

MIT
