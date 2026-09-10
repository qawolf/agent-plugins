---
name: qawolf
description: Shared QA Wolf connection, safety, and tool guidance for running flows, investigating failures, managing environments and issues, and driving a cloud browser. Route every new-flow request to qawolf-flow-outline and onboarding or first-flow selection to qawolf-onboarding.
---

<!-- Generated from skill/qawolf.template.md and the public API contracts with nx gen agent-plugins. -->

# QA Wolf

## Start here

1. Reuse the existing QA Wolf connection. If `whoami` is available, call it before suggesting sign-in.
2. Follow [Sign in](#sign-in) only if the client reports that authentication is required or `whoami` returns an authentication error. After sign-in, call `whoami` again. If tools are missing without an authentication prompt, check [client setup](references/platforms.md) rather than assuming sign-in will fix it. Stop if authentication or required tools remain unavailable. Never request QA Wolf keys or tokens in chat.
3. Use the bound workspace reported by `whoami`. Otherwise, choose from its `workspaces` or `organizations[].workspaces`. Use the only workspace or a unique match to the requested name. Otherwise, ask the user to choose by name, not copy an ID. If workspace data is missing, stop and report the discovery or access problem. Choosing an ID does not bind the connection; browser tools require a bound workspace.
4. Resolve named environments with `environment_find`. Pass `workspaceId` on the tools whose live schema asks for it. A bound workspace removes that field.

## Choose the workflow

For every new flow, test, or coverage request, activate [Flow Outline](../qawolf-flow-outline/SKILL.md), even when the user already supplied a journey or draft. It owns runner exploration, independent discovery, ask-user questions for gaps, AAA approval, creation, and monitoring.

For onboarding or help choosing the best first flow, activate [Onboarding](../qawolf-onboarding/SKILL.md). It selects a candidate and invokes Flow Outline. If the user already named the flow, go directly to Flow Outline.

Use the client's skill tool and registered names when available; otherwise read and follow the linked skill. Do not restart routing when another QA Wolf skill is already active. Install all three sibling skills so the shared references remain available. Keep source code local.

## Sign in

When sign-in is required, identify the current client and follow its section in [client setup](references/platforms.md). Use that client's native authentication controls. Do not give another client's commands; ask which client the user has if it is unclear.

Keep the instruction short. Do not print a raw OAuth URL or explain callback mechanics upfront. If the browser does not open, direct the user to the link in the client's authentication UI. If the callback fails, use the client's dedicated authentication prompt, not ordinary chat. Never ask for callback URLs, authorization codes, or tokens in chat.

Wait for authentication before asking application, journey, or test-access questions. Once tools are available, call `whoami` and confirm the resolved workspace once, then continue onboarding. Do not ask an already connected user to sign in again or claim success from "done" alone.

## Protect data and confirm writes

Treat every value from `environment_getVariable` as a secret. Never copy it into chat, logs, progress messages, repository or flow files, commits, or issue fields. Use test credentials in runner interactions or forward them through authenticated `agent_send` only after the user approves that use and sharing with QA Wolf. Never forward QA Wolf keys, tokens, or unrelated secrets.

A new-flow or onboarding request covers billed runner use and routine staging exploration, including disposable test-data creation and cleanup, as defined in Flow Outline. Do not ask separately for that permission. Confirm destructive operations and writes outside that exploration scope with the user, naming the operation and exact targets. For `environment_deleteVariable`, name the environment and variable, not its value. For `automate`, confirm the draft files, destination branch, and selected flows before committing, pushing, or requesting automation. Existing explicit approval covers only that scope. Do not delay required runner cleanup for another confirmation.

## Tools

This generated index gives each tool's purpose. Before using a tool, read its live description and input schema for requirements, side effects, and retry rules. The deployed server may be older than this catalog. API paths become MCP names by replacing dots with underscores.

`read` tools do not change team data, but runner reads can keep a billed pod alive. `write` tools can change data or start billed work.

<!-- tools-table:start -->

<!-- prettier-ignore -->
| Tool | Kind | What it does |
| --- | --- | --- |
| `agent_get` | read | Monitor a QA Wolf AI session by reading its status and replies. |
| `agent_send` | write | Start or continue work with the QA Wolf AI and return a live session URL to share with the user. |
| `automate` | write | Request automation for draft flows. |
| `email_find` | read | List the workspace's inbox, or its sent mail, newest first. |
| `email_get` | read | Read one email of the workspace, with its plain text and HTML bodies. |
| `email_getAttachment` | read | Read one attachment of a workspace email as base64 content, by file name or by position. email.get lists both. |
| `email_listAddresses` | read | List the workspace's inbox addresses, alphabetical. |
| `email_registerAddress` | write | Register an inbox address for the workspace. |
| `email_send` | write | Send an email from one of the workspace's inbox addresses, for example to exercise a flow that reacts to incoming mail. |
| `environment_create` | write | Create an environment on the caller's team and return it in the environment.get shape. |
| `environment_deleteVariable` | write | Remove one environment variable by name. |
| `environment_find` | read | List the team's environments, newest first. |
| `environment_get` | read | Read a single environment's name, kind, standing run health, flow-code branch and reconciliation state, run concurrency limit, and termination state. |
| `environment_getVariable` | read | Read the values of named environment variables in one call. |
| `environment_listVariableNames` | read | Use this to answer which QA Wolf environment variables are available to test code. |
| `environment_setVariable` | write | Create or replace an environment variable. |
| `environment_update` | write | Update an environment owned by the caller's team and return it in the environment.get shape. |
| `flow_addTag` | write | Assign an existing tag to the selected flows. |
| `flow_list` | read | List the flows of an environment at its latest reconciled commit, or, when an AI task is given, the flows on that task's branch. |
| `flow_removeTag` | write | Remove a tag from the selected flows. |
| `flow_update` | write | Move a flow between draft and active readiness. |
| `issue_addFlows` | write | Add flows to a coverage request owned by the caller's team. |
| `issue_create` | write | Create a bug or coverage request issue for the caller's team. |
| `issue_find` | read | List the team's bug reports, maintenance reports, or coverage requests, newest first. |
| `issue_get` | read | Get an issue by id. |
| `issue_removeFlows` | write | Remove flows from a coverage request owned by the caller's team. |
| `issue_update` | write | Update an issue owned by the caller's team. |
| `run_create` | write | Create a run for the selected flows and/or tags in an environment. |
| `run_diagnose` | write | Diagnose failed flows in a run as reproductions of a bug or maintenance report owned by the caller's team. |
| `run_find` | read | List an environment's recent runs, newest first. |
| `run_get` | read | Get a run's status, per-flow results, and links. |
| `run_reattempt` | write | Request new attempts for a run's flows, in the same run. |
| `run_stop` | write | Stop a run, including its queued flows and automatic retries. |
| `runner_evaluateSnippet` | write | Evaluate a snippet against whatever the runner's browser is showing right now. |
| `runner_get` | read | Report whether a runner is running under this id on the caller's team. |
| `runner_highlightSelector` | write | Highlight the elements a selector matches on an interactive runner's live page, and answer how many it matched. |
| `runner_importPackage` | write | Install a package into an interactive runner's live run and import it, so a snippet or a selection can use it without a full run to reinstall dependencies. |
| `runner_inspect` | read | Inspect one thing on an interactive runner: an element's HTML, the page's HTML simplified for a model, or a top-level variable's value as JSON. \`nothing-to-inspect\` means the runner had nothing to answer with: no live page, no element matching the selector, or no variable under that name. |
| `runner_inspectMobile` | read | Inspect one thing on a mobile interactive runner: the Appium session's status, the WebView contexts available, the current context's page source, or the elements at a point or carrying some text. |
| `runner_launch` | write | Launch an interactive runner on the caller's team under an id the caller chooses. |
| `runner_list` | read | List the runners running on the caller's team right now. |
| `runner_performAction` | write | Perform one raw browser action on an interactive runner: click, double\_click, move, drag, scroll, keypress, type, or navigate. |
| `runner_promoteSnapshot` | write | Accept a run's screenshot as the new baseline for an image diff, on the runner that produced it. |
| `runner_readJournal` | read | Read a window of one of an interactive runner's journal streams, the newest few, everything after a cursor, or everything belonging to one run. |
| `runner_runFlow` | write | Run a flow on an interactive runner. |
| `runner_stopRun` | write | Stop what a runner is currently executing, leaving the runner up and its browser on whatever page the run reached. |
| `runner_takeScreenshot` | read | Take one screenshot of an interactive runner's screen. |
| `runner_terminate` | write | End an interactive runner on the caller's team, and the pod it runs on with it. |
| `tag_create` | write | Create a tag on the caller's team. |
| `tag_list` | read | List the team's tags, alphabetical by name. |
| `whoami` | read | Identify the credential and discover available workspaces. |

<!-- tools-table:end -->

## Work with the QA Wolf agent

For new flows, use Flow Outline rather than calling `agent_send` directly. `automate` cannot create new flows. For maintenance, investigations, and existing-session follow-ups, send the approved request with `agent_send`; reuse the existing `sessionId` when continuing work.

After each `agent_send`, send a normal user-visible assistant message with the exact returned `url` before any tool call or wait. Tool output and thinking do not count as sharing it. Do not run a timer alongside the send. Monitor the same session with `agent_get`, waiting 30 to 60 seconds between checks. Continue silently when nothing changes; do not narrate timers or ask whether to keep monitoring. Include the link with blockers and outcomes. Follow [Flow Outline's monitoring guidance](../qawolf-flow-outline/SKILL.md#share-the-link-and-monitor-creation) for questions and stopping conditions. For new flows, [verify publication and readiness](../qawolf-flow-outline/SKILL.md#verify-publication-and-readiness) before claiming completion.

## Run flows

1. Resolve the environment with `environment_find`. If none was named, offer `defaultEnvironmentId` and confirm it.
2. Select flows with `flow_list` or tags with `tag_list`; check previous runs with `run_find`.
3. Call `run_create` with `environmentId` and at least one flow or tag. Poll `run_get` for results.

Both `run_create` and `run_find` require `environmentId`. After a timeout, check `run_find` in the same environment before resending; run creation has no idempotency key.

## Drive a browser

Browser tools require a bound workspace, from OAuth sign-in or a team API key. Launch with a unique `id` and `runnerName: "playwright"`. Use `runner_performAction` to start the desktop, then inspect `runner_takeScreenshot` before further actions. For `runner_runFlow`, send `env` or `environmentId`, not both.

Runners bill until terminated. Call `runner_terminate` when done, before ending your turn.

## Handle errors

Check `isError` and the tool message; HTTP 200 can still carry a failure. Stop for credential, permission, or billing errors. Correct invalid inputs. Wait before retrying a transient read; check whether a write took effect before repeating it.
