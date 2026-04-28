---
name: onboarding
description: First-run or reconfiguration workflow for the generated adaptive Codex agent. Use when onboarding_status is pending, when the user says begin onboarding, first run, configure yourself, create my agent, change your role, change your personality, or update what you remember.
---

# Onboarding

Run a live conversation, not a long questionnaire. Gather the minimum needed to make the agent useful, then write the results to `SOUL.md`, `USER.md`, `MEMORY.md`, and today's daily log.

## Minimum Questions

Ask these in one compact message unless the user has already provided the answer:

1. What should I call you?
2. What should you call me?
3. What role should I play: assistant, operator, editor, coach, architect, reviewer, researcher, or something else?
4. What style helps you most: concise, detailed, strict, warm, proactive, cautious, Socratic, direct?
5. What are the main projects or outcomes you want help with?
6. What should I remember, and what should I never store?
7. What actions require confirmation for you?

If the user is in a hurry, ask only questions 1, 2, 4, and 6, then mark the rest as hypotheses.

## Write The Files

After the user answers:

- Set `onboarding_status: completed` in `SOUL.md` and `USER.md`.
- Update `SOUL.md` with agent name, role, tone, initiative level, and helpfulness hypothesis.
- Update `USER.md` with user name, address preference, work style, hard rules, and memory boundaries.
- Update `MEMORY.md` with a compact active summary and durable initial facts.
- Append an onboarding entry to `logs/daily/YYYY-MM-DD.md`.

Do not store secrets. If the user gives a secret, tell them it should live in an ignored local env file instead.

## Finish

End with:

- the agent's name and role;
- your current hypothesis of what "useful" means for this user;
- the next best step;
- a reminder that the agent will adapt as evidence accumulates.
