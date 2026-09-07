# Create the first flow

Choose one useful user journey and give the user a link to QA Wolf's work. Login can be a good first story, but choose from the app rather than assuming.

## Confirm QA Wolf access

Complete the skill's setup checks: `whoami`, the intended workspace, and available `agent_send` and `agent_get` tools. Stop if any check fails. Follow [platform setup](platforms.md) for API-key configuration outside chat; OAuth is not available.

Supply `workspaceId` for organization or user credentials. Resolve IDs through available tools rather than guessing. QA Wolf authentication does not sign into the test application.

## Agree on the story and target

Read only enough local documentation, routes, screens, and test descriptions to identify a small journey. Keep source code local. If the repository or behavior is unclear, ask.

Propose the story in user terms, with an observable result: "A test user signs in and reaches their account dashboard." Confirm the story and target URL together. A URL found in documentation is only a candidate; the app URL and QA Wolf environment ID are separate choices.

Prefer staging. Production requires explicit approval of the URL, dedicated test account, and allowed actions. Do not use ordinary customer accounts, make purchases, send messages, or change customer data without approval.

## Arrange test access

Ask only for what the story needs:

- Base URL, entry route, user role, and starting state.
- Dedicated test credentials, SSO, MFA, email-code, or network requirements.
- Tenant, seed data, feature flags, expected result, and cleanup.

Ask for credentials through an approved secure channel, or request permission to search a specific source and environment. Search only that source, read relevant entries, and confirm the account is for testing. Do not dump secret files, search unrelated accounts, or bypass missing access.

Never echo passwords in progress messages or write them into repository files or public issues. Prefer a credential reference that QA Wolf can resolve. Otherwise send only approved test credentials through the authenticated MCP call. Never send QA Wolf API keys, OAuth tokens, or unrelated secrets.

Before starting, confirm approval to create the flow, use the target and account, and share the required access with QA Wolf. Permission to find credentials is not permission to start testing.

## Send the request

Call `agent_send` with the confirmed `workspaceId` when required and the selected `environmentId` when known. Omit `sessionId` for new work; reuse it for follow-ups.

Describe behavior for someone who can use the app but has not read its code. Include only relevant, confirmed details; remove unused fields and unresolved placeholders:

```text
Create one end-to-end flow for: <approved story>.
Target: <confirmed URL>.
Access: <approved test credentials or accessible reference>.
Starting state: <role, tenant, entry page, and setup>.
Steps: <visible user actions>.
Success: <observable result>.
Constraints: <access requirements, prohibited actions, and cleanup>.
If access fails or essential context is missing, ask before proceeding.
```

Do not send source, code snippets, diffs, test code, configuration files, archives, or a repository summary. Translate local findings into the behavior this flow must cover.

If the request times out, do not blindly resend it. Use `agent_get` if you have the session ID. Otherwise report the uncertain outcome and resolve it before risking duplicate work.

## Share and follow the result

Share the exact returned `url` immediately and retain `sessionId`. Report acceptance, not completed flow creation. If no URL arrives, say so rather than constructing one.

Poll `agent_get` every 30 to 60 seconds. Summarize new replies without repeating credentials. On `waiting-for-you`, answer from confirmed context or ask the user for missing decisions, access, or permission. Reply with `agent_send` in the same session.

Stop on `completed`, `failed`, or `cancelled`. Link the session and report the confirmed outcome. Completion alone does not prove a flow was created or passed. If you cannot keep monitoring, say so and leave the link; do not promise background work.
