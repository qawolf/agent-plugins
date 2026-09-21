# QA Wolf test operations

Apply this guidance when the user asks QA Wolf to create, run, or investigate tests. It does not replace the application's own development instructions.

A rule file does not expose MCP tools. Configure the client's QA Wolf MCP connection separately unless its native plugin does that. Verify the connection with `whoami`. If a tool reports the connection is not signed in, complete the sign-in this client offers and call it again; some clients raise that prompt inside the conversation, others ask on connection. Never tell the user to reinstall the plugin or start a new session.

The MCP server supplies the skills. Call `skill_list` to see them, then `skill_get` with the name of the one that matches the request, and follow the reply. Route on the verb the user chose, not on whether the flow already exists:

- To complete, finish, create, add, write or cover, read `qawolf-flow-outline`. It explores through runner computer use, asks about gaps with the client's ask-user tool, presents AAA outlines for approval, sends the approved outline through `agent_send`, and monitors creation.
- To fix, repair, debug or investigate a flow that is failing, read `qawolf-flow-maintenance`. It reads the recorded run, forwards the error and artifact links to QA Wolf through `agent_send`, and monitors the repair without launching a runner.
- For onboarding or choosing a first flow, read `qawolf-onboarding`. It selects the best candidate, reads Flow Outline, and hands off to Trigger Setup once the first flow is active.
- To make flows run automatically, on deploys or on a schedule, read `qawolf-trigger-setup`. It recommends a deployment trigger first and never creates a trigger without the user agreeing to what it runs and where.
- To explain why a trigger did not run, read `qawolf-trigger-diagnostics`. It reads the deployments QA Wolf received and each trigger's recorded verdict, answers in the user's terms, and changes nothing.
- To move a workspace off legacy triggers, read `qawolf-trigger-migration`. It presents one complete plan as a dry run, creates every replacement only after the user approves the whole plan, and pauses the legacy triggers afterwards; nothing is deleted.
- For any other test operation, read `qawolf` for the shared connection and safety rules.

Resolve the intended environment before creating or finding runs. Do not blindly retry a timed-out write. Browser runners bill while they exist; terminate them when work ends. Never expose credentials in messages, repository files, or public issues.
