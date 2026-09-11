# QA Wolf test operations

Apply this guidance when the user asks QA Wolf to create, run, or investigate tests. It does not replace the application's own development instructions.

Load `skills/qawolf/SKILL.md` for shared connection and safety rules. Install the sibling `qawolf-flow-outline`, `qawolf-flow-maintenance` and `qawolf-onboarding` skills too. A project may keep these under `.agents/skills/` or its client's native skill location.

A rule or skill file does not expose MCP tools. Configure the client's QA Wolf MCP connection separately unless its native plugin does that. Verify the connection with `whoami`. If a tool reports the connection is not signed in, complete the sign-in this client offers and call it again; some clients raise that prompt inside the conversation, others ask on connection. Never tell the user to reinstall the plugin or start a new session.

Route on the verb the user chose, not on whether the flow already exists. To complete, finish, create, add, write or cover, invoke `qawolf-flow-outline` or read `skills/qawolf-flow-outline/SKILL.md`. It explores through runner computer use, discovers context independently, asks about gaps with the client's ask-user tool, presents AAA outlines for approval, sends the approved outline through `agent_send`, and monitors creation. Keep source code local and share the returned session URL immediately.

To fix, repair, debug or investigate a flow that is failing, invoke `qawolf-flow-maintenance` or read `skills/qawolf-flow-maintenance/SKILL.md`. It reads the recorded run, forwards the error and artifact links to QA Wolf through `agent_send`, and monitors the repair without launching a runner.

For onboarding or choosing a first flow, invoke `qawolf-onboarding` or read `skills/qawolf-onboarding/SKILL.md`. It selects the best candidate and invokes Flow Outline. If the user already named the flow, use Flow Outline directly.

Resolve the intended environment before creating or finding runs. Do not blindly retry a timed-out write. Browser runners bill while they exist; terminate them when work ends. Never expose credentials in messages, repository files, or public issues.
