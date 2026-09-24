---
name: qawolf-start
description: Use before any QA Wolf work, including onboarding an application, choosing a first test, outlining or creating a flow, running flows, reading run results, repairing a failing flow, setting up triggers, and driving the QA Wolf cloud browser. Routes to the skill that covers the request, which the QA Wolf MCP server serves through skill_list and skill_get.
---

# Start with QA Wolf

The QA Wolf skills come from the MCP server rather than from this plugin, so what you read is always current. Read them before doing the work.

1. Call `skill_list`. It answers every skill with the description that says when to use it.
2. Pick the one whose description matches what the user asked for.
3. Read it with `skill_get` and follow it. The reply carries the whole skill, so nothing else needs fetching.
4. Read the `qawolf` skill too. It is the shared one: connection checks, workspace selection, how the user sees your messages, and the safeguards around data and writes.

A link of the form `../<skill>/SKILL.md` inside a skill names another skill. Read it by that name with `skill_get`.

## What holds whatever you are doing

Settle the workspace before acting on anything. `whoami` reports it. Every tool that takes `workspaceId` requires it, so pass it on every call rather than waiting for a refusal to tell you.

Runners bill for as long as they exist. Call `runner_terminate` once the work is done, before ending your turn, except for a runner you handed to QA Wolf with `agent_send`'s `runnerId`, which QA Wolf ends itself.

A question ends your turn. Ask it, then stop. Anything written before a tool call is folded into a work log the user rarely opens, so a question asked mid-work is one they never see.
