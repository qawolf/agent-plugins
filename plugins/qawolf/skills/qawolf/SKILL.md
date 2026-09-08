---
name: qawolf
description: Use QA Wolf MCP tools to onboard a repository, request end-to-end coverage, run flows, investigate failures, manage environments and issues, or drive a cloud browser. Use for first-flow requests and questions about QA Wolf tests.
---

<!-- Generated from skill/qawolf.template.md and the public API contracts with nx gen agent-plugins. -->

# QA Wolf

## Start here

1. Complete [client setup](references/platforms.md), then start a fresh session. Installation alone does not authenticate. Most clients open a browser for OAuth sign-in on the first connection.
2. Call `whoami` and confirm the identity and workspace. Stop if authentication fails or required tools are missing. Never request QA Wolf keys or tokens in chat.
3. If `whoami` reports several `workspaces` and no single bound workspace, ask the user which one to work in. Browser tools stay unavailable until a workspace is bound.
4. Resolve named environments with `environment_find`. Pass `workspaceId` on the tools whose live schema asks for it. A bound workspace removes that field.

For onboarding or a first flow, read [Onboarding](references/onboarding.md) before collecting access or calling `agent_send`. Keep source code local.

## Tools

This generated index gives each tool's purpose. Before using a tool, read its live description and input schema for requirements, side effects, and retry rules. The deployed server may be older than this catalog. API paths become MCP names by replacing dots with underscores.

`read` tools do not change team data, but runner reads can keep a billed pod alive. `write` tools can change data or start billed work.

<!-- tools-table:start -->

<!-- prettier-ignore -->
| Tool | Kind | What it does |
| --- | --- | --- |
| `agent_get` | read | Read what the QA Wolf AI has said and whether it is still working. |
| `agent_send` | write | Ask the QA Wolf AI to do a piece of work in plain language, such as covering a user journey, investigating a failing run, or fixing a broken flow. |
| `automate` | write | Request automation for draft flows. |
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
| `flow_update` | write | Move a flow between draft and active readiness. |
| `issue_addFlows` | write | Add flows to a coverage request owned by the caller's team. |
| `issue_create` | write | Create a bug or coverage request issue for the caller's team. |
| `issue_find` | read | List the team's bug reports, maintenance reports, or coverage requests, newest first. |
| `issue_get` | read | Get an issue by id. |
| `issue_update` | write | Update an issue owned by the caller's team. |
| `run_create` | write | Create a run for the selected flows and/or tags in an environment. |
| `run_diagnose` | write | Diagnose failed flows in a run as reproductions of a bug or maintenance report owned by the caller's team. |
| `run_find` | read | List an environment's recent runs, newest first. |
| `run_get` | read | Get a run's status, per-flow results, and links. |
| `run_reattempt` | write | Request new attempts for a run's flows, in the same run. |
| `runner_evaluateSnippet` | write | Evaluate a snippet against whatever the runner's browser is showing right now. |
| `runner_get` | read | Report whether a runner is running under this id on the caller's team. |
| `runner_highlightSelector` | write | Highlight the elements a selector matches on an interactive runner's live page, and answer how many it matched. |
| `runner_importPackage` | write | Install a package into an interactive runner's live run and import it, so a snippet or a selection can use it without a full run to reinstall dependencies. |
| `runner_inspect` | read | Inspect one thing on an interactive runner: an element's HTML, the page's HTML simplified for a model, or a top-level variable's value as JSON. \`nothing-to-inspect\` means the runner had nothing to answer with: no live page, no element matching the selector, or no variable under that name. |
| `runner_inspectMobile` | read | Inspect one thing on a mobile interactive runner: the Appium session's status, the WebView contexts available, the current context's page source, or the elements at a point or carrying some text. |
| `runner_launch` | write | Launch an interactive runner on the caller's team under an id the caller chooses. |
| `runner_performAction` | write | Perform one raw browser action on an interactive runner: click, double\_click, move, drag, scroll, keypress, type, or navigate. |
| `runner_promoteSnapshot` | write | Accept a run's screenshot as the new baseline for an image diff, on the runner that produced it. |
| `runner_readJournal` | read | Read a window of one of an interactive runner's journal streams, the newest few, everything after a cursor, or everything belonging to one run. |
| `runner_runFlow` | write | Run a flow on an interactive runner. |
| `runner_stopRun` | write | Stop what a runner is currently executing, leaving the runner up and its browser on whatever page the run reached. |
| `runner_takeScreenshot` | read | Take one screenshot of an interactive runner's screen. |
| `runner_terminate` | write | End an interactive runner on the caller's team, and the pod it runs on with it. |
| `tag_create` | write | Create a tag on the caller's team. |
| `tag_list` | read | List the team's tags, alphabetical by name. |
| `whoami` | read | Identify the team, organization, or user authenticated on the MCP connection. |

<!-- tools-table:end -->

## Request coverage

Require both `agent_send` and `agent_get`. If either is missing, stop; `automate` cannot create new flows.

1. Send the approved journey, target URL, access details, and constraints with `agent_send`. For new work, omit `sessionId`.
2. Share the returned `url` immediately. Acceptance is not completed flow creation.
3. Poll `agent_get` with the returned `sessionId` every 30 to 60 seconds. Replies accumulate; report only new information.
4. On `waiting-for-you`, answer from confirmed context or ask the user. Reply through `agent_send` with the same `sessionId`.
5. Stop on `completed`, `failed`, or `cancelled`. Report what QA Wolf confirmed, not an inferred passing run.

If sending times out, do not resend blindly. Use `agent_get` when the session ID is known; otherwise report the uncertain outcome before risking duplicate work.

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
