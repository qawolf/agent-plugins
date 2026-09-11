---
name: qawolf
description: Shared QA Wolf connection, safety, and tool guidance for running flows, investigating failures, managing environments and issues, and driving a cloud browser. Read an app.qawolf.com link instead of opening it. Route on the verb the user chose, not on whether the flow exists: complete, finish, create, add, write or cover goes to qawolf-flow-outline, fix, repair, debug or investigate goes to qawolf-flow-maintenance, and onboarding or first-flow selection goes to qawolf-onboarding.
---

<!-- Generated from skill/qawolf.template.md and the public API contracts with nx gen agent-plugins. -->

# QA Wolf

## Start here

1. Call `whoami` first. If it or any tool reports that the connection is not signed in, complete the sign-in this client offers and call the tool again. If no QA Wolf tool is available at all, this client has no QA Wolf connection: tell the user to add `https://app.qawolf.com/api/mcp` as an MCP server, and point them at [client setup](references/platforms.md) for their client. Never tell the user to reinstall the plugin or start a new session. Never call a tool name that is not in the table below. Never request QA Wolf keys or tokens in chat.
2. Confirm the identity and workspace `whoami` reports. Stop if sign-in cannot be completed or required tools are missing. See [client setup](references/platforms.md) when a client needs its connection configured by hand.
3. Act on the `workspace` that `whoami` reports, which it reports when the connection reaches exactly one. Otherwise choose from `workspaces`, which lists every workspace this connection can act on. Each entry carries the `organizationName` that owns it, so name a workspace by both when two share a name, and the `slug` that names it in a link. When the user gave a link, its slug decides, and only an exact match to an entry's `slug` counts. If no entry matches it, say the connection cannot reach the workspace that link names and stop; do not fall back to the only workspace, because acting on a different one is worse than not acting. Without a link, use the only workspace or a unique match to the requested name, and otherwise ask the user to choose by name. Never ask them to paste an id. If workspace data is missing, stop and report the discovery or access problem. Pass the one you chose as `workspaceId`, and a browser tool binds to it for that call.
4. Settle the environment the same way, with `environment_find`. Use the one the user named, or the `environmentId` a link carries, or the only environment the workspace has. When more than one remains, list them by name and ask. Pass `workspaceId` on the tools whose live schema asks for it. A bound workspace removes that field.

Workspace and environment follow one rule: exactly one is chosen for you, several means you ask. Do not guess either, and do not settle for the default when the workspace has more than one environment, because staging, preview and production are not interchangeable. Ask by name and never ask the user to paste an id. Use the client's ask-user tool where it has one, and ask before starting the work, not after.

## Reading a QA Wolf link

A QA Wolf link is data to read, not a page to open. Parse it:

```text
https://app.qawolf.com/<workspaceSlug>/environments/<environmentId>/automate/ide?file=<path>
https://app.qawolf.com/<workspaceSlug>/environments/<environmentId>/flows/<flowId>
```

The first path segment is the workspace `slug`, which `whoami` reports for every workspace. The segment after `environments/` is the `environmentId` that `agent_send`, `run_create` and `flow_list` take. So a link alone resolves both, with no lookup and no navigation.

Never open, fetch, browse or navigate to `app.qawolf.com`. It needs a browser session this connection does not have, so it reaches a sign-in page and the work stops there. Everything the link carries is already in the link. The only exception is a user asking you to open that page for them.

This restricts QA Wolf's own app and nothing else. Opening the customer's site or app is what the runner tools are for, and exploring it is expected when a skill calls for it. When you do not know which deployment to open, which login to use, or what credentials it takes, ask the user.

## Choose the workflow

A QA Wolf request is one of three things. The verb the user chose decides the route, so read that first. Whether the flow already exists does not decide it, and neither does a pasted link.

| The user says                                                                     | Route to                                                |
| --------------------------------------------------------------------------------- | ------------------------------------------------------- |
| complete, finish, create, add, write, build, cover, request coverage              | [Flow Outline](../qawolf-flow-outline/SKILL.md)         |
| fix, repair, debug, investigate, diagnose, troubleshoot, unbreak, "it is failing" | [Flow Maintenance](../qawolf-flow-maintenance/SKILL.md) |
| onboard, get started, pick a first flow                                           | [Onboarding](../qawolf-onboarding/SKILL.md)             |

The question behind the table is whether something is broken. "Complete this flow" names a draft that exists and is unfinished, where nothing has failed, so it is creation and goes to Flow Outline. "Fix this flow" names something that ran and went wrong, so it goes to Flow Maintenance. A link to a flow says nothing either way, since both skills work from one.

Onboarding selects a candidate and invokes Flow Outline; if the user already named the flow, go straight to Flow Outline. When the verb is genuinely ambiguous, such as "update this flow", ask the user which they mean before routing.

Every one of these ends in `agent_send`, which is what asks QA Wolf to do the work. The skills differ in what they establish first, so route once and let the skill you picked do the sending.

When the request points at a file — a test plan, a spreadsheet of journeys — upload it first with [Share a file](#share-a-file) and carry the returned path into the workflow, rather than pasting its rows or asking the user to retype them.

Use the client's skill tool and registered names when available; otherwise read and follow the linked skill. Do not restart routing when another QA Wolf skill is already active. Install all four sibling skills so the shared references remain available. Keep source code local.

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
| `file_requestDownload` | read | Get a URL for reading a file out of the caller's team storage. |
| `file_requestUpload` | write | Get a URL to put a file into team storage: a spreadsheet of journeys, anything too large to paste. |
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
| `runner_inspect` | read | Inspect one thing on an interactive runner: an element's HTML, the page's HTML simplified for a model, or a top-level variable's value as JSON. |
| `runner_inspectMobile` | read | Inspect one thing on a mobile interactive runner: the Appium session's status, the WebView contexts available, the current context's page source, or the elements at a point, carrying some text, or matching a selector. |
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
| `trigger_create` | write | Create a trigger. |
| `trigger_delete` | write | Delete a trigger permanently. |
| `trigger_find` | read | List the team's triggers, newest first. |
| `trigger_get` | read | Get one trigger by id. |
| `trigger_pause` | write | Pause a trigger so it stops firing. |
| `trigger_resume` | write | Resume a paused trigger. |
| `trigger_update` | write | Replace a trigger's configuration. |
| `whoami` | read | Identify the credential and list every workspace this connection can act on, with the organization that owns each one. |

<!-- tools-table:end -->

## Work with the QA Wolf agent

Creating or finishing a flow goes through Flow Outline, and repairing one goes through Flow Maintenance. `automate` cannot create new flows. For an investigation or a follow-up in a session you already opened, send with `agent_send` directly and reuse the existing `sessionId`.

After each `agent_send`, send a normal user-visible assistant message with the exact returned `url` before any tool call or wait. Tool output and thinking do not count as sharing it. Do not run a timer alongside the send. Monitor the same session with `agent_get`, waiting 30 to 60 seconds between checks and passing that session's previous `nextCursor` as `cursor`, so a check reads only what is new. Continue silently when a check returns no replies; do not narrate timers or ask whether to keep monitoring. Include the link with blockers and outcomes. Follow [Flow Outline's monitoring guidance](../qawolf-flow-outline/SKILL.md#share-the-link-and-monitor-creation) for questions and stopping conditions. For new flows, [verify publication and readiness](../qawolf-flow-outline/SKILL.md#verify-publication-and-readiness) before claiming completion.

## Share a file

Send a file when the request is bigger than a message: a spreadsheet of journeys to cover, a fixture a flow uploads. Never paste its contents into `agent_send`.

1. Call `file_requestUpload` with the file name. It answers a `path` and an `uploadUrl`.
2. Upload the bytes from the shell, not through a tool, sending the returned `contentType` as the `Content-Type` header: `curl -H 'Content-Type: application/octet-stream' --upload-file "journeys.csv" "<uploadUrl>"`. That header is part of the signature, so the file's own MIME type gets a 403. The URL expires, so upload right after you request it.
3. Call `agent_send` with the returned `path` in `filePaths`. QA Wolf reads the file from storage; a path with no file behind it is refused.

Uploading the same name again replaces the file, so pick a name nothing else uses unless replacing is what you want. `file_requestDownload` answers a URL for reading one back.

## Run flows

1. Resolve the environment with `environment_find`, following [Start here](#start-here). When several remain, ask by name and say which one `defaultEnvironmentId` points at.
2. Select flows with `flow_list` or tags with `tag_list`; check previous runs with `run_find`.
3. Call `run_create` with `environmentId` and at least one flow or tag. Poll `run_get` for results.

Both `run_create` and `run_find` require `environmentId`. After a timeout, check `run_find` in the same environment before resending; run creation has no idempotency key.

## Drive a browser

Browser tools require a bound workspace, from OAuth sign-in or a team API key. Launch with a unique `id` and `runnerName: "playwright"`. Use `runner_performAction` to start the desktop, then inspect `runner_takeScreenshot` before further actions. For `runner_runFlow`, send `env` or `environmentId`, not both.

Runners bill until terminated. Call `runner_terminate` when done, before ending your turn.

## Handle errors

Check `isError` and the tool message; HTTP 200 can still carry a failure. Stop for credential, permission, or billing errors. Correct invalid inputs. Wait before retrying a transient read; check whether a write took effect before repeating it.
