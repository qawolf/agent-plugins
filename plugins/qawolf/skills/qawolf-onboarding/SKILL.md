---
name: qawolf-onboarding
description: Use when the user wants to onboard an application to QA Wolf, get started with QA Wolf, choose their first test, or find the best first flow. Select a useful, achievable onboarding journey, then invoke qawolf-flow-outline for runner exploration, AAA approval, draft publication, an independent run, repair when needed, and activation after success. Once the first flow is active, invoke qawolf-trigger-setup so the workspace ends with automation, not just coverage. A specific new-flow request goes directly to qawolf-flow-outline, and a failing existing flow goes to qawolf-flow-maintenance.
---

# Onboarding

Choose the best first flow for this application, then hand it to Flow Outline. Do not maintain a second exploration or implementation workflow here.

This skill is for an application with no coverage yet. A user who named the flow they want goes straight to [Flow Outline](../qawolf-flow-outline/SKILL.md), and one whose existing flow is failing goes to [Flow Maintenance](../qawolf-flow-maintenance/SKILL.md).

## Choose the first flow

Apply the shared [connection checks](../qawolf/SKILL.md#start-here) and [data and write safeguards](../qawolf/SKILL.md#protect-data-and-confirm-writes). Reuse known context and skip sign-in when already connected. Ask for the application URL or goal only if missing; use the client's ask-user tool when available. Never request credentials in chat; a login the flow needs goes through the [environment variables page](../qawolf/SKILL.md#protect-data-and-confirm-writes).

If the user already named the flow, use that choice and invoke Flow Outline immediately. Do not run a separate selection exercise or require the user to repeat the goal.

Otherwise, recommend one candidate using the app's purpose, the user's priorities, available test access, and known constraints. Prefer a core user outcome with a short repeatable path, a visible success state, and little destructive setup or cleanup. Login is a candidate, not the automatic choice. Avoid payment, messaging, or customer-data changes unless explicitly approved.

State why the candidate is useful and achievable. Treat it as a hypothesis until runner exploration verifies it. If essential product context or business priorities are missing, use the ask-user tool for that gap, then select one concrete candidate before invoking Flow Outline. Do not replace browser exploration with source inspection or ask the user to map the application for you.

## Invoke Flow Outline

Activate `qawolf-flow-outline` through the client's skill tool, using the registered plugin-qualified name where required. If the client cannot invoke skills, read and follow [Flow Outline](../qawolf-flow-outline/SKILL.md) directly. Loading a skill does not delegate to the remote QA Wolf agent.

Pass the application target, proposed or user-selected journey, selection rationale, that this is the application's first flow, known workspace and environment, approved access references, permission boundaries, prior observations, and unresolved gaps. Do not pass secret values or invent missing context.

Flow Outline owns the flow work: runner computer-use exploration, independent discovery, ask-user questions for gaps, AAA presentation, approval for the full lifecycle, `agent_send`, draft publication, independent runs, repairs, and readiness. It may refine the candidate based on observations before presenting the outline. Do not call `agent_send` yourself or launch a second creation session after the handoff. Selecting a candidate is not approval to create it. Finish the approved batch, then report its results; another onboarding journey needs its own visible outline and approval.

## Hand off to Trigger Setup

Onboarding is not finished when the first flow is active, because a workspace with coverage and no automation runs nothing on its own. Once Flow Outline reports the flow active, invoke `qawolf-trigger-setup` the same way you invoked Flow Outline, or read and follow [Trigger Setup](../qawolf-trigger-setup/SKILL.md) directly.

Pass what is already settled: the workspace, the environment, the active flow, and what you learned about the application and how it is deployed. Trigger Setup owns the rest: reading the repository, choosing between a deployment trigger and a schedule, and the user's agreement before anything is created. Do not choose a trigger kind or create a trigger here, and do not repeat its questions afterwards.

A user who declines automation ends onboarding with the flow report; tell them triggers are available whenever they want the flow running on its own. A flow that stayed a draft has nothing for a trigger to run, so skip the handoff and say why.
