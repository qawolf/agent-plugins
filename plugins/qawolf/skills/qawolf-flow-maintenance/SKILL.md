---
name: qawolf-flow-maintenance
description: Use when something is wrong with an existing QA Wolf flow, test, or run and the user wants it put right. The verb decides: fix, repair, debug, investigate, diagnose, troubleshoot, unbreak, or update a flow to match a changed application. Covers "fix this flow", "fix the error in this flow", "investigate this flow", "this test is failing", "this flow is flaky", "why did this run fail", and a failing run or run attempt id. Read the recorded failure, then hand the repair to QA Wolf and monitor it. Complete, finish, create, add, or cover means nothing is broken, so that belongs to qawolf-flow-outline even when the user pastes a link to an existing draft.
---

# Flow Maintenance

Repair a flow that already exists. The failure has already happened and QA Wolf recorded it, so the context comes from reading that record, not from exploring the application again.

This skill does not create flows. Check the verb before going further. If the user asked to complete, finish, create, add, write or cover, they want creation, so stop here and switch to [Flow Outline](../qawolf-flow-outline/SKILL.md), even though the flow they named already exists and even though they pasted a link to it. Choosing a first flow for a new application goes to [Onboarding](../qawolf-onboarding/SKILL.md). If you are already inside one of those, stay there.

## Establish the target

Read the shared [connection checks](../qawolf/SKILL.md#start-here), [link reading](../qawolf/SKILL.md#reading-a-qa-wolf-link), and [data and write safeguards](../qawolf/SKILL.md#protect-data-and-confirm-writes). Reuse the workspace, environment, and approvals already settled in this conversation.

A pasted link gives you the workspace slug and the environment id without any lookup. Do not open it. Without a link, settle both the way the shared [connection checks](../qawolf/SKILL.md#start-here) describe, asking by name whenever more than one workspace or environment is left.

Then identify the flow. `flow_list` with `includeDrafts: true` names the flows, since the flag defaults to false and a draft is otherwise left out; `run_find` names recent runs. If the user described a symptom without naming a flow, ask which one instead of guessing between similar names.

## Read the recorded failure

Gather the evidence with read tools. `run_diagnose` is not one of them, since it writes and returns no diagnosis of its own; it has its own step below.

- `run_find` for recent runs of the flow, to see whether this fails every time or intermittently.
- `run_get` for the failing run. Each failed flow carries `failure.error`, the raw error text from the run itself, and `attempts` with a `logsUrl`, `traceUrl` and `videoUrl` for each one.
- `issue_get` on `failure.diagnosis.issueId` when `run_get` reports a diagnosis, since QA Wolf has already reached a verdict of `bug` or `maintenance` on this failure. Otherwise `issue_find` for an open issue covering it, so you do not open a second thread.

Do not launch a runner. `runner_launch` starts a billed pod, and the recorded run already holds the error, the trace, the logs and the video. Stop reading once you can say which step failed and what the run reported. Two or three reads is normal.

If the run history shows the flow passing and failing without a code change, say it looks intermittent and include that in what you send. If no run exists at all, there is nothing recorded to repair, so ask the user what they saw.

## Link the failure to an issue

`run_diagnose` records failed flows as reproductions of an issue that already exists, and that issue's `type` sets the verdict: `bug` when the application is broken, `maintenance` when the test needed updating. It writes to both the run and the issue, which is why it sits outside the reading above.

Use it when the user wants this failure tracked, or when the failures you read reproduce an issue `issue_find` already turned up. Name the issue and the flows and confirm before calling, because a flow already diagnosed against another issue moves to the one you name, which overwrites someone else's triage. Create the issue with `issue_create` first when none fits. A coverage request cannot be diagnosed, so use `issue_addFlows` for one.

Diagnosing is optional and separate from the repair. Skip it and go straight to sending when the user only asked for the flow to be fixed.

## Send the repair

Confirm with the user before sending when the fix is not obviously wanted, for example when the flow is failing because the application changed on purpose and the test may be correct to fail. Otherwise send.

Call `agent_send` on its own, with no monitoring call or timer alongside it. Pass the `environmentId` you resolved, and `workspaceId` when the live schema asks for it. Omit `sessionId` to open a new session, or reuse it to continue one.

Send what you read, not a restatement of the user's request. Pass on every fact `run_get` gave you, because QA Wolf reads the trace and the logs from these links and starts from your account of the failure:

```text
Fix this failing flow.
Flow: <name>, <id>.
Environment: <name>, <id>.
Run: <run id>.

Error, verbatim from the run:
<the failure.error string, unedited, including its call log>

Attempts: <n>, all failed / <n> of <m> failed, <first start> to <last completion> UTC.
Trace: <traceUrl>
Logs: <logsUrl>
Video: <videoUrl>
Step reached: <the last step the run got to, when the logs or trace name it>.
Screen at failure: <what the failure showed, when you can tell>.
Existing verdict: <bug or maintenance, issue <id>, when run.get carried a diagnosis>.
History: <fails every run since <date>, or intermittent across <n> runs>.
Constraints: <anything the fix must not change>.
Validate the fix, then publish to this environment's flow-code branch.
Report what changed, the validation result, and the published commit.
Ask if the application changed on purpose and the test should be retired instead.
```

Quote `failure.error` in full and unedited. Do not summarise it, and do not stop at its first line, because the call log under it names the selector that timed out. Two flows can fail with byte-identical error text for entirely unrelated reasons, so the message alone does not identify the cause; the trace and the state of the screen are what separate them. That is why the links matter more than your reading of them.

Artifact links stay valid for about a day, and a link 404s when that attempt produced no such artifact. Read `run_get` again if the send is delayed, and drop a line whose value you do not have instead of sending a placeholder. `agent_send` carries text only, so paste the values and never attach or paste a file.

Never send credentials, source code, or configuration files. Reference test access QA Wolf can resolve for itself.

## Share the link and monitor

After the send, your next action is a normal assistant message containing the exact returned `url`. Tool output and thinking do not count. Then monitor with `agent_get` and the same `sessionId`, following the shared [monitoring rules](../qawolf/SKILL.md#work-with-the-qa-wolf-agent): 30 to 60 seconds between checks, silence while nothing changes, no narration of waiting.

On `waiting-for-you`, answer from what you already read where you can, and use the client's ask-user tool for anything you cannot. Relay the answer through `agent_send` in the same session.

## Confirm the repair

A final reply is not proof. Before saying the flow is fixed, confirm the flow still exists at the readiness it had, using `flow_list` with `includeDrafts: true` so a repaired draft is still listed, and report the validation result QA Wolf gave along with the published commit. Report agent-reported validation as agent-reported unless you verified it.

Do not activate a flow that was a draft before the repair, and do not change readiness as part of a fix. If the repair left something unfinished, name that specific step instead of calling the work done.
