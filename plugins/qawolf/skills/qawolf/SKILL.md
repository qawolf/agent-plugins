---
name: qawolf
description: Onboard a repository to QA Wolf, choose its first user story, request end-to-end test coverage, run flows, and drive a cloud browser through the qawolf MCP tools. Use when the user wants to get started with QA Wolf, create their first flow, have tests written or run, investigate a failure, answer a QA Wolf question, or reproduce a problem in a browser.
---

# QA Wolf

The `qawolf` MCP server exposes the QA Wolf public API as tools. Every tool name is the API contract path with dots replaced by underscores, so `run_create` is `run.create`. Apex authenticates the credential on the connection. Each tool acts as that team, organization, or user.

## Before you start

1. Connect through the MCP client's OAuth 2.1 sign-in when the deployed connection supports it. The API-key-only preview still uses `QAWOLF_API_KEY`, configured outside the chat as described in the plugin README.
2. Call `whoami` to verify which team, organization, or user the connection acts as. If authentication fails, stop and ask the user to sign in or fix the client configuration before continuing. Never ask for OAuth tokens or QA Wolf API keys in chat.
3. If the user names an environment, resolve it with `environment_find` after authentication and before starting work.

## Onboard a repository

For onboarding or a first-flow request, read [Onboarding](references/onboarding.md) before collecting application access or calling `agent_send`. It covers choosing a story from the local codebase, confirming staging or a production test account, obtaining approved credentials, sending instructions without source code, and sharing the session URL while monitoring QA Wolf's work.

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

- Missing or rejected credential: ask the user to sign in again through the MCP client, or check `QAWOLF_API_KEY` if using the API-key-only preview.
- Billing prevented the call: tell the user and stop.
- Credential authenticated but is not allowed: for `runner_*`, the user needs a team API key.
- Rate limited or temporarily unavailable: wait before retrying a read. Do not repeat a write without checking whether it took effect.
- Invalid input: the message names the field. Correct it and call again.
