---
name: qawolf-trigger-setup
description: Use when the user wants QA Wolf flows to run automatically. Covers "set up triggers", "run my tests on every deploy", "run these flows nightly", "automate my test runs", and connecting a CI pipeline or deployments to QA Wolf. Onboarding invokes it once a first flow is active, and a user with existing flows invokes it directly; the decision procedure is the same either way. Recommends a deployment trigger first, through GitHub or GitLab Deployments or a deployment.reportStatus call from CI, and finishes with a scheduled trigger when the pipeline will not change. Migrating a workspace off legacy triggers is a different task and does not belong here.
---

# Trigger Setup

Set up the trigger that makes a workspace's flows run without anyone asking. A trigger fires on a deployment or on a schedule; this skill chooses which, agrees on what it will run, creates it through the trigger tools, and verifies it where verification is possible.

This skill configures new automation only. A workspace moving off legacy triggers needs a migration, which this skill does not cover; say so and stop instead of improvising one.

## Check the connection and scope

Read the shared [connection checks](../qawolf/SKILL.md#start-here) and [data and write safeguards](../qawolf/SKILL.md#protect-data-and-confirm-writes). Require `trigger_create`, `trigger_find`, `environment_find`, and `flow_list`.

When Onboarding invoked this skill, reuse everything it passed: the workspace, the environment, the flow that just became active, and what it learned about the application. Do not re-ask any of it. On a direct request, settle the workspace and environment the way the shared checks describe.

Call `trigger_find` before proposing anything. A trigger that already covers the request means the work is adjusting or resuming it, not creating a duplicate; report what exists and ask what the user wants changed.

## Read the pipeline before asking

When this session has the customer's repository open, look before asking. What is there decides which rung of the ladder below is realistic:

- A GitHub workflow whose jobs declare `environment:`, a deploy action that creates GitHub Deployments, or a hosting provider such as Vercel that creates them on its own means the pipeline already emits deployment events.
- A GitLab CI job with the `environment:` keyword means the same for GitLab.
- An existing `deployment.reportStatus` call in CI means QA Wolf is already told about deploys directly.
- A CI config that deploys but creates no deployment record means the pipeline would need a change for options 1 and 2.

Without a repository in context, ask the user the same questions instead: what deploys their application, whether anything creates GitHub or GitLab deployments today, and whether they can add a step to CI. A plain chat with no repository is a normal entry point, not a blocker.

Whether a code host is connected to the workspace is separate from what the pipeline emits. Call `codeHostIntegration_find`: it says whether GitHub or GitLab is connected, and its top-level `settingsUrl` is the workspace's integrations settings page, present whether or not anything is connected. Use it for whether an integration exists and which provider; read its live schema for anything more.

The two findings separate the failure modes that need different advice. No integration connected means the first step is [connecting one](#connect-the-code-host). An integration connected while the pipeline creates no deployments means the code host is silent and the gap is in the pipeline, not the connection.

State what you inferred and confirm it before acting on it. An application can deploy from somewhere you cannot see, so an inference is a hypothesis, not a finding.

## Choose the trigger kind

Recommend the best rung the customer can reach, in this order:

1. **GitHub or GitLab Deployments.** The richest signal: QA Wolf learns the branch, the commit, and the environment of every deploy. When the integration is connected and the pipeline already emits deployment events, the pipeline may need no change at all, but confirm what it emits first, because a shared preview name or an unmatched environment name fails silently. A pipeline that does not emit them yet can start, per [emitting deployment events](references/deployment-events.md).
2. **`deployment.reportStatus`.** For a pipeline that cannot emit deployment events, a CI step reports the deploy to QA Wolf directly, with a `providerDeploymentId`, a `status` of `success`, and the environment it deployed to.
3. **A scheduled trigger.** Runs the flows on a cadence. The only option that changes nothing in the customer's pipeline.

Recommend a deployment trigger first and say why: the flows run exactly when the application changed, against the deploy that changed it. But a schedule is a legitimate choice, not a consolation; a user who simply wants nightly runs gets one without being argued out of it.

Options 1 and 2 usually require the customer to change their own pipeline, and always a real deploy to prove the events arrive. Say that plainly before the user commits to either. When the user declines to touch the pipeline, or the pipeline change stalls, finish with a scheduled trigger now so the workspace has working automation, and note that a deployment trigger can replace or join it later. Do not end the request with flows and no trigger.

## Connect the code host

Deployment events reach QA Wolf through the installed integration, so the first rung needs one connected for the provider that hosts the pipeline. When the user wants deployment events and `codeHostIntegration_find` reports nothing for their provider, walk them through connecting it. Connecting is the price of the first rung, not a requirement: a user who does not want to install an app or mint a token right now moves down the ladder to `deployment.reportStatus`, or to a schedule if the pipeline stays untouched.

- **GitHub:** the user enables the integration on the workspace's integrations settings page (the `settingsUrl` the tool reports), which installs the QA Wolf GitHub App and selects the repositories it covers. Selection matters: a repository the app does not cover sends no events, so the deploying repository must be among them. Afterwards, confirm by calling `codeHostIntegration_find` again instead of assuming the install worked.
- **GitLab:** the same settings page takes a GitLab group access token with the Maintainer role and the `api` scope, which the user creates in GitLab following GitLab's own group-access-token documentation. Maintainer specifically: QA Wolf refuses a lesser token, because lower roles cannot create the webhooks and pipeline checks it needs. Never request credentials in chat: the user creates the token in GitLab and pastes it into the settings page directly, and it never passes through you.

## Agree on what will run

Every trigger names an action: the flows or tags it runs, and for a deployment trigger, which deployments it fires for. Settle this with the user before creating anything:

- Which flows: specific flows from `flow_list`, or a tag from `tag_list` so newly tagged flows join automatically. A workspace fresh out of onboarding usually runs its one active flow.
- A name: `trigger_create` requires one, so propose one the user would recognize later, naming what runs and when.
- Where: the environment for a schedule, or the match fields for a deployment trigger: `environmentIds` or `environmentPattern`, `deployTargetPattern`, `branchPattern`. Every pattern supplied must match, and supplying none fires on every deployment the workspace reports, which is rarely what a multi-environment pipeline wants.

Static and preview deployments want different triggers:

- A static environment such as staging or production usually needs only a simple match (the environment's name, or a deploy-target pattern when the URL is stable and distinctive) and explicit, comprehensive coverage: a tag or all flows.
- Preview deployments need a pattern matching the shape their deployments actually use: `pr-*`, `preview/*`, `review/*`, or whatever the workflow emits. Read the workflow or ask; never guess a convention. This is the trigger for a generative action, `kind: "generativeSuite"` on `trigger_create`'s `action`, which names no flows or tags because QA Wolf picks them from the pull request's changes, and whose optional `instructions` carry guidance for that choice. The right trade for a small change, and the only trigger it works on: generative selection needs the deployment to resolve to a pull request (a preview deploy of a pull request's head commit does, a push to a static branch does not) and skips every deployment without one. Offer to tailor `instructions` when creating it, and read the live schema for the exact action shape.

A team deploying both ways gets two triggers by default, one of each. One trigger matching everything looks simpler and is worse: a pull request should not run everything staging runs, and a generative action on it would skip on every static deploy.

Present the plan as one plain sentence covering what runs, where, and when it fires, then confirm with the client's ask-user tool. Never call `trigger_create` before the user has agreed to that sentence. A trigger starts billed runs on its own from then on, which is exactly why it needs the agreement and exactly what makes it useful.

## Create a deployment trigger

Call `trigger_create` with `kind: "deployment"`, the agreed action, and the agreed match fields.

Then close the loop on the events:

- Pipeline already emitting: confirm the emitted environment name matches the environment the user intends and that previews are isolated per pull request, using the checks in [emitting deployment events](references/deployment-events.md), before treating the pipeline as done. Then ask the user to deploy, or wait for the next deploy, and confirm with `run_find` that a run appeared for it.
- Pipeline needs to emit provider events: ask whether they deploy previews as well as long-lived environments, because the answer changes both the workflow to recommend and the triggers to create. Then walk the user through [emitting deployment events](references/deployment-events.md). In particular, the deployment's environment name must match the QA Wolf environment they intend, and previews must be isolated per pull request. Say that only a real deploy verifies it end to end.
- Pipeline reports directly: give the user the `deployment.reportStatus` call to add to CI, reading the live schema for its exact fields. A deployment's first `success` report is what evaluates triggers. With the user's agreement you can send one test report yourself to prove the wiring before their CI change lands; it fires the trigger for real, so say that it starts billed runs.

When a deploy happened and no run appeared, the question is why the trigger did not fire: did a deployment reach QA Wolf at all, and which condition failed. Answer those two in order before changing anything about the trigger.

A deployment trigger that has never seen a deployment is configured, not verified. Report which of the two it is; do not claim verification a deploy has not provided.

## Create a scheduled trigger

A schedule needs a cadence, an environment, and for a daily cadence a `timeOfDay` with a `timezoneId`. The cadence and time come from the user: when they said "nightly", propose a concrete time and confirm it. An hourly schedule fires on the hour unless `minuteOfHour` says otherwise.

Never fill in a timezone the user did not choose. You may propose one you have evidence for, such as the timezone their repository or conversation indicates, but the user confirms it before it goes into the trigger. A daily run in the wrong timezone fires during the customer's business hours and looks like a malfunction.

Call `trigger_create` with `kind: "schedule"` once cadence, time, timezone, and environment are all confirmed. The response's `nextScheduledAt` says when it next fires; check that it matches what the user asked for before reporting success.

## Report in the user's terms

Describe what now happens, not the object that was created: "your smoke-tagged flows run in Staging every time your pipeline reports a successful deploy", or "your checkout flow runs daily at 02:00 New York time". Include the trigger's `url` so the user can see it, and mention that `trigger_pause` turns it off without deleting it. When a pipeline change is still pending on the customer's side, restate what remains and how they will know it worked: the first matching deploy produces a run.
