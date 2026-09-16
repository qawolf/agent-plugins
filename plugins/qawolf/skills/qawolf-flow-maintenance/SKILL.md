---
name: qawolf-flow-maintenance
description: Use when something is wrong with an existing QA Wolf flow, test, or run and the user wants it put right. The verb decides: fix, repair, debug, investigate, diagnose, troubleshoot, unbreak, or update a flow to match a changed application. Covers "fix this flow", "fix the error in this flow", "investigate this flow", "this test is failing", "this flow is flaky", "why did this run fail", and a failing run or run attempt id. Read the recorded failure, hand the repair to QA Wolf, require validation before publication, run the published repair, and preserve the flow's readiness. Complete, finish, create, add, or cover means nothing is broken, so that belongs to qawolf-flow-outline even when the user pastes a link to an existing draft.
---

# Flow Maintenance

Repair a flow that already exists. The failure has already happened and QA Wolf recorded it, so the context comes from reading that record, not from exploring the application again.

This skill does not create flows. Check the verb before going further. If the user asked to complete, finish, create, add, write or cover, they want creation, so stop here and switch to [Flow Outline](../qawolf-flow-outline/SKILL.md), even though the flow they named already exists and even though they pasted a link to it. Choosing a first flow for a new application goes to [Onboarding](../qawolf-onboarding/SKILL.md). If you are already inside one of those, stay there.

## Establish the target

Read the shared [connection checks](../qawolf/SKILL.md#start-here), [link reading](../qawolf/SKILL.md#reading-a-qa-wolf-link), and [data and write safeguards](../qawolf/SKILL.md#protect-data-and-confirm-writes). Reuse the workspace, environment, and approvals already settled in this conversation.

A pasted link gives you the workspace slug and the environment id without any lookup. Do not open it. Without a link, settle both the way the shared [connection checks](../qawolf/SKILL.md#start-here) describe, asking by name whenever more than one workspace or environment is left.

Then identify the flow. `flow_list` with `includeDrafts: true` names the flows, since the flag defaults to false and a draft is otherwise left out; record the selected flow's readiness so the repair preserves it. `run_find` names recent runs. If the user described a symptom without naming a flow, ask which one instead of guessing between similar names.

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
Validate the complete flow before publishing, then publish only the validated repair to this environment's flow-code branch.
Report what changed, the validation result, and the published commit.
If the flow still fails or cannot be repaired, do not publish the repair. Report the blocker and leave the environment's published code unchanged.
Ask if the application changed on purpose and the test should be retired instead.
```

Quote `failure.error` in full and unedited. Do not summarise it, and do not stop at its first line, because the call log under it names the selector that timed out. Two flows can fail with byte-identical error text for entirely unrelated reasons, so the message alone does not identify the cause; the trace and the state of the screen are what separate them. That is why the links matter more than your reading of them.

Artifact links stay valid for about a day, and a link 404s when that attempt produced no such artifact. Read `run_get` again if the send is delayed, and drop a line whose value you do not have instead of sending a placeholder. `agent_send` carries text only, so paste the values and never attach or paste a file.

Never send credentials, source code, or configuration files. Reference test access QA Wolf can resolve for itself, and when a repair needs a login QA Wolf does not have, send the user to the [environment variables page](../qawolf/SKILL.md#protect-data-and-confirm-writes) and name the variable.

## Share the link and monitor

After the send, your next action is a normal assistant message containing the exact returned `url`, repeated in the last message of the turn. Tool output and thinking do not count. See [how the user sees your messages](../qawolf/SKILL.md#how-the-user-sees-your-messages). Then monitor with `agent_get` and the same `sessionId`, following the shared [monitoring rules](../qawolf/SKILL.md#work-with-the-qa-wolf-agent): 30 to 60 seconds between checks, silence while nothing changes, no narration of waiting.

On `waiting-for-you`, answer from what you already read where you can, and use the client's ask-user tool for anything you cannot. Relay the answer through `agent_send` in the same session.

## Verify the published repair

A final reply is not proof. Require QA Wolf to report that the complete flow passed validation before accepting a publication. If it reports a blocker or incomplete validation, report that result and stop without asking it to publish partial maintenance work.

After QA Wolf publishes a validated repair:

1. Call `flow_list` with `includeDrafts: true`, match the exact flow ID, confirm that reconciliation includes the reported commit when available, and verify that readiness still matches the value recorded before the repair.
2. Call `run_create` with the exact `flowId` and poll `run_get` until terminal. Check `excludedFlows` before polling. A flow listed there was not run, so report the exclusion and stop instead of accepting a passing result as a verified repair.
3. If the run passes, report the validation, published commit, run URL, flow URL, session URL, and preserved readiness. A terminal passing run counts as success even when its attempts include earlier failures.
4. If the run fails, send the complete error and every available trace, log, and video URL to QA Wolf through the same session. Ask it for another concrete repair, with the same requirement to validate before publishing. Monitor, verify reconciliation, and rerun.
5. Continue while QA Wolf has a concrete corrective step. Stop when it identifies an application problem, missing access, inability to repair, or another failure with no new corrective step. Report the blocker and latest evidence without activating the flow or asking QA Wolf to publish a failing repair.

Never change readiness as part of maintenance. Do not weaken the flow's intended assertions to make a run pass.
