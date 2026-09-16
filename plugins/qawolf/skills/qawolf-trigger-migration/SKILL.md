---
name: qawolf-trigger-migration
description: Use when a workspace still runs legacy triggers and the user wants them moved to the current trigger model. Covers "migrate my triggers", "move off legacy triggers", and "upgrade to global triggers". Reads every legacy trigger across the workspace's environments, presents one complete migration plan as a dry run, creates every replacement only after the user approves the whole plan, and pauses the legacy triggers afterwards. Setting up new automation belongs to qawolf-trigger-setup, and a trigger that misfired is a diagnosis question, not a migration; this skill is for working legacy automation that must keep working through the move.
---

# Trigger Migration

Move a workspace's legacy triggers to the current trigger model without a coverage gap. The automation being migrated already works and pays for itself, so the standard for this skill is not "create equivalent triggers" but "the customer's flows keep running on the same occasions throughout".

## One trigger cuts the whole team over

The first unpaused current-model trigger switches the entire workspace off the legacy deployment path at once — per team, not per trigger. At that instant every legacy deployment trigger not yet recreated goes dark, silently. So migration is never an incremental loop of "convert one, check it, convert the next". The order is fixed: read everything, plan everything, get approval on the whole plan, create all replacements, and only then pause legacy triggers. Any unpaused new-model trigger trips the switch regardless of kind — a scheduled trigger counts — so migrating "just the schedules first" is not a smaller safe step; it opens the same gap.

The two legacy families fail in opposite directions, and the plan must say so:

- **Legacy deployment triggers fed by GitHub or GitLab deployment events** stop firing on their own the moment the first new trigger exists. Left unmigrated, they are a silent coverage gap.
- **Legacy scheduled triggers keep firing regardless** — and so do deployment triggers fed by the legacy `deploy_success` call, which the cutover does not gate. Until these are explicitly paused, the workspace gets duplicate runs.

A consequence worth stating plainly: a single legacy trigger that cannot be mapped blocks the whole execution. Creating "just the easy ones" cuts the team over and turns the hard one into the silent gap. Stop and resolve it with the user first, or record their explicit decision to drop it.

## Check the connection and scope

Read the shared [connection checks](../qawolf/SKILL.md#start-here) and [data and write safeguards](../qawolf/SKILL.md#protect-data-and-confirm-writes). Require `trigger_create`, `trigger_find`, `trigger_get`, `trigger_pause`, `environment_find`, `flow_list`, `tag_list`, and `run_find`.

The legacy routes are not MCP tools — they are frozen internal endpoints reached over raw HTTP with the workspace's API key, from the API keys page under the workspace's settings. Read the key from the shell environment (pipelines that used the legacy CI SDK usually export `QAWOLF_API_KEY` already). Never ask the user to paste it into chat and never echo it; when it is not on hand, ask the user to export it in the shell or point you at where their CI keeps it. A client with no shell tool cannot make the raw calls itself: give the user the exact requests to run and have them paste the responses back, rather than skipping the reads or guessing.

## Read everything first

The plan is built entirely from reads. Collect all of it before proposing anything:

1. **Existing current-model triggers**, with `trigger_find`. An unpaused one means the cutover already happened: legacy deployment triggers are already dark, the gap already exists, and the plan should say so and move fast. It may also mean a previous migration stopped halfway — diff what exists against the legacy triggers before recreating anything.
2. **Environments**, with `environment_find`. Legacy triggers are listed per environment — there is no team-wide listing — so fan out over every static environment. Transient preview environments carry nothing to migrate.
3. **Legacy triggers**, one read per environment:

   ```text
   GET https://app.qawolf.com/api/trpc/trigger.getMany?input=<encoded>
   Authorization: Bearer <API key>
   ```

   where `<encoded>` is the URL-encoded form of `{"json":{"filter":{"environmentId":"<id>"},"include":{"tags":true}}}`. The triggers come back under `result.data.json` as an array (a sibling `meta` key annotates dates; the values in `json` are already readable). Each trigger's `type` is `scheduled`, `generic` (a deployment trigger), or `pr-testing-button`.

   A failure comes back as an `error` object instead of a `result`, carrying a message and code — treat it as a failed read, never as an empty list. The first read also proves the key: the environment ids come from `environment_find` in the target workspace, so a key belonging to a different workspace fails authorization there rather than listing anything. An authorization failure means the wrong key, not nothing to migrate.

4. **How deployments reach QA Wolf today**, for any legacy deployment trigger — the next section says why this read often decides the shape of the whole plan.

Record what was read verbatim; the verification step diffs against it.

## Migrate the deployment reporting first

A trigger migration is often blocked behind a deployment-reporting migration. Customers notify QA Wolf of deploys in several distinct ways, and they are not interchangeable: calling the legacy endpoint directly (`POST https://app.qawolf.com/api/webhooks/deploy_success`), the legacy CI SDK (`@qawolf/ci-sdk` in a package.json), the `qawolf/notify-qawolf-on-deploy-action` GitHub Action — three faces of the same `deploy_success` path, and each greppable in a repository by exactly those strings — or real GitHub or GitLab deployment events, or `deployment.reportStatus` on the public API. Current-model triggers evaluate only the last two. A deploy reported only through the legacy path is invisible to the new triggers, so for that customer the pipeline must change before the deployment side of this migration can work at all.

Establish which path the customer actually uses before planning any deployment trigger. When this session has their repository open, look: workflow files and CI config say it directly, and far more reliably than asking — the reading approach is [Trigger Setup's](../qawolf-trigger-setup/SKILL.md#read-the-pipeline-before-asking). When the pipeline needs to change, the change itself is Trigger Setup's ground too: [emitting deployment events](../qawolf-trigger-setup/references/deployment-events.md) or a `deployment.reportStatus` call, planned as an explicit step of this migration rather than an aside. On GitLab, transient is a naming rule rather than a flag: preview environments must be named under `review/` or every one accumulates permanently — a migration that matches preview deploys on GitLab checks the names against [long-lived versus transient](../qawolf-trigger-setup/references/deployment-events.md#long-lived-versus-transient) before trusting the setup.

A customer already emitting real GitHub or GitLab deployment events who also calls `deploy_success` has a duplicate reporting path, and dropping the legacy call is part of the cleanup — but verify coverage before advising it. A very common shape is deployment events for long-lived environments only, with previews reported through `deploy_success`; telling that customer to drop the call silently kills their preview testing. Check whether the deployment events cover previews too, and say plainly that the answer decides whether the legacy call can go.

## Map each trigger

The goal is equivalent effect, not a faithful port — several legacy fields have no counterpart, and forcing them through produces triggers that look right and fire wrong. When a legacy trigger's intent has no clean expression in the current model, stop and ask the user what the trigger was for; never approximate silently. Often the honest answer is a pipeline change rather than a cleverer mapping: a distinguishable environment name, a deploy target on the deployment, or real deployment events make the intent expressible — propose that concretely, per [Trigger Setup](../qawolf-trigger-setup/SKILL.md#read-the-pipeline-before-asking) and its [deployment-events reference](../qawolf-trigger-setup/references/deployment-events.md), instead of leaving the user with a bare "cannot map".

- **What runs.** Legacy tags become `tagNames` on the action. A legacy trigger with no tags ran the environment's flows wholesale, and the current model requires the action to name flows or tags — confirm with the user what it actually covered, then propose a tag (so future flows join) or explicit `flowIds`, saying which trade-off you chose. `adaptiveFlowSelection` maps to a `generativeSuite` action, which needs the deployment to resolve to a pull request and therefore belongs only on a preview-style trigger; [Trigger Setup](../qawolf-trigger-setup/SKILL.md#agree-on-what-will-run) covers when that action fits and how to shape it.
- **Scheduled cadence.** `repeatMinutes` of 1440 becomes a daily trigger; 60 becomes hourly, with `minuteOfHour` derived from `startAt` the same way daily derives its time — left out, it defaults to 0 and silently moves a quarter-past trigger to the top of the hour. 720 becomes two daily triggers twelve hours apart, because one trigger carries at most one schedule. Any other cadence has no equivalent: stop and ask.
- **Time and timezone.** A daily trigger needs `timeOfDay` and `timezoneId`. Derive the wall-clock time from the legacy `startAt` rendered in the legacy `timezoneId`; when the legacy trigger has no timezone, its time is UTC — present it as UTC and let the user confirm or move it. Never invent a timezone the data does not carry.
- **Deployment matching.** Legacy `deploymentType` was an opaque identifier the pipeline echoed back; the current model matches on environment, deploy-target pattern, and branch pattern instead, so translate the intent: which deploys was this trigger for? Usually the trigger's own environment as the match. Branch scoping lives in `uncheckedVcsDeploymentBranchesInput`: a single plain entry becomes `branchPattern`, but the legacy field is a comma-separated list of globs whose leading `-` negates the whole list, and `branchPattern` is one glob with neither — treat a comma list or a negation like an unmappable cadence and stop. A `codeHostingServiceRepository` rule of `by-id` also has no public equivalent; mapped to the environment alone it would fire for every connected repository, so stop and ask there too.
- **PR-button triggers** (`type: "pr-testing-button"`) drove the pull-request testing button, a shape the current model no longer supports. They migrate to automatic PR testing: a deployment trigger matching the preview shape with a `generativeSuite` action, per [Trigger Setup](../qawolf-trigger-setup/SKILL.md#agree-on-what-will-run). That is a behavior change worth confirming — testing moves from on-demand button presses to automatic on every matching preview deploy.
- **Already paused legacy triggers** are left alone and listed as such. If the user wants one carried over anyway, create its replacement and immediately `trigger_pause` it so it arrives off.

## Present the plan as a dry run

The complete plan, produced with reads only, is the deliverable of the first pass — and the whole first run against a real customer. It contains, in the user's terms:

- every legacy trigger found, per environment, with its family and paused state;
- for each, the replacement it becomes — name, what runs, when it fires — or the question blocking it;
- which legacy triggers will be paused explicitly and which stop on their own;
- anything unusual: an existing unpaused current-model trigger, a pipeline that may not report deployments the new model sees, a cadence with no equivalent.

Present it and stop. Nothing is created until the user approves the whole plan, and approval is their move after reading it — never folded into the message that starts creating. A user who only wants to see where they stand gets exactly this plan and no writes at all.

## Create all, then pause

After approval, in this order:

1. Create every replacement with `trigger_create`, checking each response — a schedule's `nextScheduledAt` should match the plan.
2. Pause every legacy scheduled trigger, promptly, since duplicates run until this lands:

   ```text
   POST https://app.qawolf.com/api/trpc/trigger.pause
   Authorization: Bearer <API key>
   Content-Type: application/json

   {"json":{"triggerId":"<legacy trigger id>"}}
   ```

   A successful pause returns an empty result; the proof it took is the re-read in the verify step, not the response body.

3. Pause the legacy deployment triggers the same way. Those fed by deployment events already stopped at step 1, so this makes the workspace's state legible; those fed by `deploy_success` keep matching for as long as the pipeline keeps calling it, so for them pausing is as necessary as for the schedules.

When execution breaks partway, the safe direction reverses: "stop and ask" is right everywhere before approval and wrong here, because the first create already cut the team over. A `trigger_create` that fails after another succeeded means finish the remaining creates and then report what failed — an open coverage gap outranks a tidy pause. A pause that fails after the creates leaves coverage intact and duplicates running: retry, and if it keeps failing, name the legacy triggers still live and say duplicates continue until they are paused. A session that ends between approval and completion resumes through the verify step — re-read everything, diff against the approved plan, and finish what is missing before reporting.

Nothing is deleted at any point. Pausing is reversible — the same route with `trigger.resume` brings a legacy trigger back — which is also the rollback story if something is wrong: pause the new triggers with `trigger_pause` and resume the legacy ones.

## Verify and report

Verify your own work by re-reading, not by trusting the create responses. Call `trigger_find` and diff the new triggers against the plan — cadence, time, timezone, matching, and what runs. Re-run the legacy reads and confirm every trigger the plan said would be paused now carries a `pausedAt`. Report any difference, including a legacy trigger that changed between the first read and now.

Then report in the user's terms: what now runs on which occasions, what was paused and that it is reversible, and what to watch. For schedules, the next firing time. For deployments, the proof is the next deploy: a run should appear for it (`run_find`), and until one real deploy has produced one, the deployment side is migrated but not yet verified — say which of the two it is.
