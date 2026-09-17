---
name: qawolf-trigger-diagnostics
description: Use when a trigger should have fired and did not, or fired differently than the user expected. Covers "why didn't my trigger run", "my deploy didn't start any tests", "no run appeared for my pull request", and "why did this deploy run the wrong flows". Reads the deployments QA Wolf received and each trigger's recorded verdict, and explains the outcome in the user's terms. Diagnosis only; it changes nothing, proposes the fix, and hands the change to qawolf-trigger-setup. Creating new automation belongs to qawolf-trigger-setup, moving off legacy triggers belongs to qawolf-trigger-migration, and a run that happened and failed belongs to qawolf-flow-maintenance.
---

# Trigger Diagnostics

Answer "why didn't my trigger run?" and "why did it run the wrong thing?" from recorded evidence. QA Wolf keeps every deployment it received and, for each one, a per-trigger verdict from the moment it was evaluated, so the answer is usually on record: nothing arrived, or a deployment arrived and a named condition failed, or a trigger matched and something stopped the run, or a different trigger than the user assumed created the run. This skill finds which one it is and says it in the user's terms. It changes nothing: the fix, once agreed, is [Trigger Setup](../qawolf-trigger-setup/SKILL.md)'s ground or the customer's own pipeline.

## Check the connection and scope

Read the shared [connection checks](../qawolf/SKILL.md#start-here) and [data and write safeguards](../qawolf/SKILL.md#protect-data-and-confirm-writes). Require `deployment_find`, `deployment_listTriggerEvaluations`, `trigger_find`, and `codeHostIntegration_find`; `trigger_get`, `run_get`, and `codeHostIntegration_listRepositories` fill in details. Everything here is a read. Call no write tool from this skill, including `trigger_resume`: a paused trigger is a finding to report, not a state to correct.

## Start from the occasion, not from ids

The user names the deploy the way they see it — a pull request, a commit, a branch, "yesterday's release to staging" — and must never need a QA Wolf id. Resolve their words yourself:

1. When this session has the customer's repository open, resolve the occasion there first: a pull request gives its head commit sha and branch, a release gives its tag's commit, a bare "my deploy" gives the branch and rough time. Without a repository, ask for whichever of branch, commit, environment, or time the user knows; any one is enough to search on.
2. Call `deployment_find` and scan the pages, newest first, for a deployment whose `commitSha`, `branch`, `deployTarget`, or `environmentName` matches, with `deployedAt` near the time in question. Keep paginating until the pages are older than the occasion; the default page is recent history, not all of it.
3. Read the deployment you found in full before judging anything. `environmentName` says where it actually landed, which is not always where the user believes it went: a pipeline emitting an unexpected name lands deployments in a silently created environment the triggers never target, per [the environment-name contract](../qawolf-trigger-setup/references/deployment-events.md#the-environment-name-is-the-contract).

Also call `trigger_find` now, so you know which trigger the user means and its current state before reading verdicts about its past.

Three outcomes, three paths: the deployment is found, so [read its verdicts](#read-the-verdicts); other deployments exist but this one is missing, so this deploy [never arrived](#when-no-deployment-arrived); the workspace has no deployments at all, which is the same section's strongest form — tell the user the integration or the pipeline is the problem, never show them an empty list as the answer.

## Read the verdicts

`deployment_listTriggerEvaluations` reports what happened when the deployment was evaluated, and its vocabulary is the diagnosis:

- **`not-evaluated`**: triggers were never checked, because only a deployment's first `success` report evaluates them. The deployment's own `status` says what was reported instead: `pending` means the pipeline created the deployment and never reported success — the deploy step failed, or the success report is missing from the pipeline; `failure` means the deploy itself failed, and no trigger should have fired.
- **`evaluated`** carries one verdict per trigger that existed at evaluation time. Verdicts are a snapshot: editing or deleting a trigger later does not change them, a verdict with no `triggerId` belongs to a trigger deleted since, and a trigger created after the deployment has no verdict at all — it appears only in `trigger_find` and will be evaluated on the next deployment, which answers the user who created a trigger and expected it to cover a deploy from before it existed.

For the trigger the user cares about, the verdict is one of three:

- **`not-considered`** with `trigger-paused`: the trigger was paused when the deployment was evaluated. Check `trigger_get` for whether it still is; resuming it is usually the whole fix, and it is the user's move, not yours.
- **`not-considered`** with `not-a-deployment-trigger`: the trigger has no deployment conditions — a schedule, typically — so no deploy can ever fire it. A user expecting deploy-driven runs from it needs a deployment trigger, which is [Trigger Setup](../qawolf-trigger-setup/SKILL.md#choose-the-trigger-kind)'s job.
- **`did-not-match`**: name the condition that failed, quoting its recorded `reason`. Condition sets are ORed and the conditions inside a set are ANDed, so the explanation is the failed condition in each set — usually one set, one condition, one plain sentence: "the deployment reported into `pr-417` and the trigger matches `staging`". Compare the snapshot against `trigger_get` before proposing an edit, since the trigger may have changed since.
- **`matched`**: matching is not running, so read the `run` outcome. `ran` names the run — show it with `run_get`, which also settles "the wrong flows ran": the evaluations say which trigger created which run, so attribute before anyone edits a trigger, and a run that happened and failed is [Flow Maintenance](../qawolf-flow-maintenance/SKILL.md)'s ground, not a trigger problem. `starting` means run creation is still in progress; check `run_find` again shortly. `did-not-run` carries the recorded reason, and a `supersededByRunId` means an earlier delivery of the same deployment already produced that run — coverage, not a gap, so show that run. `unknown` means QA Wolf has no record of what followed the match: say exactly that and treat it as a [question for QA Wolf](#when-the-records-run-out), not something to guess at.

## When no deployment arrived

A missing deployment means the arrival path is broken somewhere between the pipeline and QA Wolf, and `codeHostIntegration_find` splits that path in two:

- **No integration for the provider that hosts the pipeline**, and no `deployment.reportStatus` call in CI: QA Wolf cannot hear about deploys at all. That is the whole answer — the integration or the reporting call comes first, and connecting one is [Trigger Setup](../qawolf-trigger-setup/SKILL.md#connect-the-code-host)'s ground.
- **An integration is connected but this deploy never arrived**: the code host is silent about it — or provider events were never this deploy's arrival path, because the pipeline reports it directly with `deployment.reportStatus` and that call failed or never ran, which a connected integration does nothing to rule out. Check `codeHostIntegration_listRepositories` — a repository the installation does not cover sends no events — then read the pipeline the way [Trigger Setup does](../qawolf-trigger-setup/SKILL.md#read-the-pipeline-before-asking): a workflow that deploys without creating a GitHub or GitLab deployment emits nothing to hear, and what a compliant pipeline must emit is in [emitting deployment events](../qawolf-trigger-setup/references/deployment-events.md). Other deployments still arriving for the workspace narrow the gap to this repository or workflow.

A pipeline that reports deploys only through the legacy path — the `deploy_success` endpoint, the legacy CI SDK, or the `notify-qawolf-on-deploy-action` — is invisible to these records and to current-model triggers even though the customer's runs may still be happening. A workspace in that state is due a migration, which is `qawolf-trigger-migration`'s job, not a diagnosis to keep re-running.

## When the records run out

The evaluation data explains matching. It does not explain everything downstream of a match or upstream of an arrival, and a diagnosis that pretends otherwise is confidently wrong. Two failure families look healthy in these records:

- **Deployments arrive but connect to nothing.** Runs happen, yet no branch or pull request shows on them and nothing posts back to the code host. The tell is deployments consistently missing `commitSha` and `branch` even though the pipeline sends them: QA Wolf is failing to resolve the repository or the pull request on its side, and no customer-visible record says why.
- **The match works and an expected side effect never happens.** Per-pull-request environments never get created although the deployments resolve pull requests, for example. A capability can be off for the workspace without anything readable saying so.

So keep two distinct findings apart: "QA Wolf received nothing" is the previous section, with a checkable cause; "QA Wolf received it but could not connect it to anything" is this one, and its cause is not in reach. For the second, report exactly what the records show and where they stop, then hand the user a precise question for QA Wolf support — the deployment's time, environment, commit, and the observed gap — instead of inventing a cause. An honest "the records end here, ask QA Wolf this" is the correct diagnosis.

## Report and hand off

Close with one plain sentence naming the single thing that failed, backed by the record it came from: "no deployment for that commit ever reached QA Wolf", "the deployment arrived but reported into `pr-417`, which the trigger's `staging` condition does not match", "the trigger was never considered because it was paused". Then propose the fix and stop:

- The trigger itself — paused, wrong conditions, wrong kind, missing — goes to [Trigger Setup](../qawolf-trigger-setup/SKILL.md) once the user agrees, with your finding carried over so nothing is re-investigated.
- The pipeline — no deployment events, a mismatched environment name, a missing success report, a shared preview — is the customer's change, guided by [emitting deployment events](../qawolf-trigger-setup/references/deployment-events.md).
- A workspace still on legacy reporting or legacy triggers goes to `qawolf-trigger-migration`.
- A gap the records cannot explain goes to QA Wolf support with the question composed above.

This skill ends with the explanation, never with a write. Even the one-call fix waits for the user.
