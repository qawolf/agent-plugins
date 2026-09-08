# QA Wolf test operations

Apply this guidance when the user asks QA Wolf to create, run, or investigate tests. It does not replace the application's own development instructions.

Load the complete `qawolf` skill and its references before starting. This distribution contains it at `skills/qawolf/SKILL.md`; a project may instead install it at `.agents/skills/qawolf/SKILL.md` or the client's native skill location.

A rule or skill file does not expose MCP tools. Configure the client's QA Wolf MCP connection separately unless its native plugin does that. Verify the connection with `whoami`; stop if the connection or required tools are unavailable. Most clients sign in with OAuth through a browser on the first connection.

For a first flow, read the onboarding reference. Keep source code local. Confirm the user story, target URL, workspace, and approved test access before sending behavioral instructions through `agent_send`. Share the returned URL and monitor the same session with `agent_get`. Do not claim acceptance means the flow is complete.

Resolve the intended environment before creating or finding runs. Do not blindly retry a timed-out write. Browser runners bill while they exist; terminate them when work ends. Never expose credentials in messages, repository files, or public issues.
