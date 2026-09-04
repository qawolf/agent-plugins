# Onboard a repository to QA Wolf

Help the user create one useful end-to-end flow, then give them a link to follow QA Wolf's work. Keep the first request small enough to explain and verify. Logging in is often a good first story, but choose it from the customer's app rather than assuming every app needs the same test.

## 1. Authenticate with QA Wolf

Use the MCP client's OAuth 2.1 sign-in flow when the deployed QA Wolf connection supports it. Let the client handle authorization, token storage, and refresh. Do not ask the user to paste an OAuth token or send one in a tool message.

OAuth 2.1 is the intended sign-in experience. If the connection is still the API-key-only preview, explain that limitation and follow the plugin README's `QAWOLF_API_KEY` setup outside the chat. Do not invent an authorization URL or claim OAuth is available before it is deployed.

Call `whoami` to verify the connection. If authentication fails, stop and ask the user to sign in or fix their client configuration before continuing. Confirm the QA Wolf workspace; an organization or user identity alone does not identify the workspace to use. `agent_send` needs `workspaceId` for organization and user credentials. Resolve the selected workspace and any named QA Wolf environment through the available tools rather than guessing IDs.

Check that the connected server exposes both `agent_send` and `agent_get`. If either is absent, explain that coverage creation needs a newer deployment. Do not substitute `automate`, which cannot create new flows.

Signing into QA Wolf does not sign into the customer's application. Treat the test application's account as a separate credential and ask for it only when the chosen story needs it.

## 2. Identify the first user story

Read the local repository's README, route definitions, relevant screens, and existing test descriptions. Inspect only enough to understand a small, valuable user journey. Keep source code local.

For a login story, identify the user role, how they reach the sign-in page, the visible steps, and the result that proves login succeeded. Prefer an observable outcome such as the account dashboard and signed-in user name, not merely the absence of an error.

Explain the proposed story in customer terms: "A test user signs in with email and password and reaches their account dashboard." Cite local evidence when useful. Ask whether this is the right first flow before starting work. If the repository is unavailable or the journey is unclear, ask for an app description instead of inventing behavior.

## 3. Confirm the target and collect access

Prefer the staging environment. Find a likely URL in project documentation or non-secret configuration, but treat it as a candidate until the user confirms it. Distinguish the app's URL from the QA Wolf environment ID; selecting one does not verify the other.

Ask the user to approve the story and target together. For example:

> I suggest starting with email-and-password login and checking that the account dashboard appears. Is this the correct staging URL? Can you provide a dedicated test account through an approved secure channel, or may I look for one in a specific source you authorize? I'll pass only the access details needed for this flow to QA Wolf.

If staging is unavailable, ask whether a dedicated production test account is appropriate. Proceed against production only after the user confirms the URL, account, and allowed actions. Do not use an ordinary customer account or perform purchases, send messages, or change real customer data without explicit approval.

Collect only what the chosen flow needs:

- The confirmed base URL and any entry route.
- The account's role and approved test credentials, if login is required.
- Any SSO, MFA, email-code, or network access requirements that QA Wolf must handle.
- Required tenant selection, seed data, feature flags, and starting state.
- The expected visible result and any cleanup or actions to avoid.

If the user authorizes credential discovery, restrict the search to the agreed source and environment. Read only relevant entries from an approved QA Wolf environment or secret store; do not dump secret files or search unrelated accounts. Confirm that a discovered account is intended for testing before using it. If access is missing, ask the user rather than bypassing authentication.

Do not echo passwords in progress messages, write them into repository files, or include them in public issues. Prefer an approved credential reference when you have verified that QA Wolf can resolve it. Otherwise, send only the approved test-account credentials through the authenticated MCP call. Never include QA Wolf OAuth tokens, API keys, or unrelated secrets.

Before sending, confirm that the user has approved creating this first flow, the target URL, the test account or access method, and sharing those access details with QA Wolf. A URL found in the repository or permission to search for credentials is not approval to start testing.

## 4. Ask QA Wolf to create the flow

Call `agent_send` once the required context and approval are in place. Supply the confirmed `workspaceId` when required and the selected `environmentId` when known. Omit `sessionId` for new work; reuse it only when continuing an existing session.

Write the `message` as instructions for someone who can use the app but has not read its code. Include the confirmed URL, approved credentials or a verified accessible reference, the user's goal, visible steps, expected result, and relevant constraints. Describe UI labels and behavior in plain language.

Use this outline, filling only the fields relevant to the approved story. Do not send unresolved placeholders:

```text
Create one end-to-end flow for: <approved user story>.
Target URL: <confirmed staging URL or explicitly approved production URL>.
Test access: <approved dedicated account credentials or verified accessible reference>.
Starting state: <entry page, role, tenant, and required setup>.
Steps: <short sequence of visible user actions>.
Success: <observable result that proves the story worked>.
Constraints: <MFA or network requirements, actions to avoid, and cleanup>.
If access fails or an essential detail is missing, ask before proceeding.
```

Do not attach or copy repository source, code snippets, diffs, test code, configuration files, or archives. Translate useful findings from the codebase into behavioral instructions instead. Send the minimum context needed for this flow, not a repository summary.

If `agent_send` times out, do not blindly send it again: the work may already have started. Use `agent_get` if a session ID is known. Otherwise, explain the uncertain outcome and resolve it before risking a duplicate request.

## 5. Share the session URL and monitor

On a successful response, give the user the exact `url` returned by `agent_send` immediately. Say that QA Wolf has accepted the request and is working; acceptance does not mean a flow has been created. Keep the returned `sessionId` for follow-up calls. If no URL is returned, report that limitation rather than constructing a link.

Poll `agent_get` with the session ID, waiting 30 to 60 seconds between calls. Replies accumulate, so summarize only new information and do not repeat credentials. If the client cannot keep monitoring, tell the user and leave them the session link rather than promising background work.

When the status is `waiting-for-you`, read the question and any choices. Answer from confirmed context, or ask the user when new credentials, permissions, or decisions are needed. Send the answer through `agent_send` with the same `sessionId`; do not start another session.

Stop polling on `completed`, `failed`, or `cancelled`. Summarize the reported result and include the session link again. Report successful flow creation only when QA Wolf's replies confirm it; do not infer that a flow passed a test run merely because the session completed.
