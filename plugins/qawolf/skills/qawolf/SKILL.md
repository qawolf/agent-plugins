---
name: qawolf
description: Ask QA Wolf for end-to-end test coverage, run flows, read what failed, and drive a live cloud browser through the qawolf MCP tools. Use when the user wants tests written or run for their app, asks what failed in QA Wolf, wants to answer a question from QA Wolf, or wants a real browser to reproduce a problem.
---

# QA Wolf

The `qawolf` MCP server exposes the QA Wolf public API as tools. Every tool name is the API contract path with dots replaced by underscores, so `run_create` is `run.create`. Apex authenticates the credential on the connection. Each tool acts as that team, organization, or user.

## Before you start

1. Call `whoami` once. It reports which team, organization, or user the credential belongs to.
2. If `whoami` reports a missing or rejected credential, stop and tell the user to set `QAWOLF_API_KEY` to a team API key from the QA Wolf app.
3. If the user names an environment, resolve it with `environment_find` before any other call.

## Request coverage

First check that the connected server exposes both `agent_send` and `agent_get`. Tool availability depends on the deployed server version. If either is absent, tell the user that this server cannot handle coverage requests yet. Do not substitute `automate`, which cannot create new flows.

When both tools are available, use `agent_send` when the user wants QA Wolf to write, fix, or investigate tests.

1. Write the message in plain language. Name the journey, the part of the app, and anything QA Wolf cannot discover on its own: test accounts, feature flags, how to reach staging.
2. `agent_send` answers as soon as the request is accepted, with a `sessionId` and a `url`. Give the `url` to the user.
3. Poll `agent_get` with that `sessionId`. Wait 30 to 60 seconds between polls. The work runs for minutes to tens of minutes.
4. If the status is `waiting-for-you`, the last reply is a question. If the reply carries `choices`, pick one or ask the user. Answer with `agent_send` and the same `sessionId`.
5. Stop polling when the status is `completed`, `failed`, or `cancelled`. Report the last reply to the user.

Replies accumulate, so each `agent_get` returns the earlier replies again. Report only the new ones.

## Run flows

1. Find flows with `flow_list`, or tags with `tag_list`.
2. Start a run with `run_create`. Send `flowIds`, `tagNames`, or both. At least one is required.
3. Read the result with `run_get`. A run takes minutes, so wait between reads.
4. Use `run_find` to look up past runs before you create a new one.

`run_create` has no idempotency key. If the call times out, call `run_find` before you send it again. Otherwise you start a second run.

## Drive a browser

The `runner_*` tools give you a live cloud browser. They need a team API key. An organization or user key gets an authorization error on every one of them.

CAUTION: A runner bills for as long as it exists. Call `runner_terminate` as soon as the work is done, and before you end your turn.

1. `runner_launch` with a unique `id` and `runnerName: "playwright"`.
2. `runner_performAction` starts the desktop. A fresh runner answers `screen-needs-a-run` to a screenshot until an action runs.
3. `runner_takeScreenshot` returns an image block. Look at it before the next action.
4. `runner_runFlow` runs flow code on the runner. Send `env` or `environmentId`, not both.
5. `runner_terminate` when you are done.

## Manage environments and issues

- `environment_setVariable`, `environment_getVariable`, and `environment_deleteVariable` manage secrets and settings per environment.
- `issue_find`, `issue_get`, `issue_create`, and `issue_update` manage QA Wolf issues.
- `environment_update` and `issue_update` need at least one field to change.

## Errors

Tool failures return `isError: true` with a text message. The transport can still return HTTP 200. Read the message rather than looking for an HTTP status in it.

- Missing or rejected credential: tell the user to check `QAWOLF_API_KEY`.
- Billing prevented the call: tell the user and stop.
- Credential authenticated but is not allowed: for `runner_*`, the user needs a team API key.
- Rate limited or temporarily unavailable: wait before retrying a read. Do not repeat a write without checking whether it took effect.
- Invalid input: the message names the field. Correct it and call again.
