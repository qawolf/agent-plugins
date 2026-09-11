# QA Wolf plugin

Use QA Wolf from your coding agent to request test coverage, run flows, inspect results, and drive a cloud browser. See [platform setup](skills/qawolf/references/platforms.md) for native plugins, portable skills, MCP configuration, and guidance-only limitations.

This is a preview distributed through the [QA Wolf plugin repository](https://github.com/qawolf/agent-plugins). It is not yet listed in the providers' official directories. The plugin signs in with OAuth.

## Connect to QA Wolf

QA Wolf clients connect to `https://app.qawolf.com/api/mcp` and sign in with OAuth through `https://signin.qawolf.com`. Codex offers the sign-in inside the conversation the first time it calls a QA Wolf tool. The ChatGPT app, Claude Code, Claude Desktop, and Gemini ask when the server is added or on first connection. Check the [preview status](https://github.com/qawolf/agent-plugins#status) before use.

No API key is needed. Do not add an `Authorization` header to the plugin's MCP entry; in Claude Code and Codex a configured header switches OAuth off and the connection fails with HTTP 401.

Where a browser sign-in cannot happen, such as CI or a container, use the API key fallback described in [platform setup](skills/qawolf/references/platforms.md). Keep any key out of shell history, source control, chats, issues, and screenshots.

OAuth reaches every workspace you are a member of, across all of your organizations. `whoami` lists them with the organization that owns each one. When there is exactly one the connection binds to it; otherwise pass `workspaceId`, and a browser tool binds to the workspace you name. A team API key is always bound to its team.

## Install in Claude Code

```text
/plugin marketplace add qawolf/agent-plugins
/plugin install qawolf@qawolf
```

Start a new session after installation. Open `/mcp`, select the QA Wolf plugin server, and choose Authenticate if sign-in is needed. Follow the browser sign-in, then return to Claude and ask it to call `whoami` to confirm your account and workspace.

Claude Code handles the callback and token storage. If the browser does not open, use the link in its authentication UI. If the redirect fails, use its dedicated authentication prompt. Do not paste callback URLs, authorization codes, or tokens into chat.

To sign in from a terminal instead, run `claude mcp login plugin:qawolf:qawolf`; the plugin-scoped name is required, and the bare `qawolf` does not resolve.

## Install in Codex

```bash
codex plugin marketplace add qawolf/agent-plugins
codex plugin add qawolf@qawolf
```

Start a new Codex session, then ask Codex to call `whoami`. It offers the sign-in inside the conversation on that first tool call; `codex mcp login qawolf` starts it by hand.

## Install in the ChatGPT app

ChatGPT does not take MCP servers from an installed plugin, so add QA Wolf as a connector once. Turn on developer mode in settings, then add an MCP server with the URL `https://app.qawolf.com/api/mcp` and no header. ChatGPT authorizes it during setup. Then ask QA Wolf for something in a new chat.

## Install in Claude Desktop

Add QA Wolf as a custom connector with the URL `https://app.qawolf.com/api/mcp` and no header, then authorize it.

## Install in Google Antigravity CLI

```bash
agy plugin install https://github.com/qawolf/agent-plugins
```

Then run `/mcp auth qawolf` to sign in. Ask the agent to call `whoami` to confirm your account and workspace.

## Other coding agents

The public repository also exposes the four sibling skills under `skills/` and a Pi package entrypoint. Install `qawolf`, `qawolf-flow-outline`, `qawolf-flow-maintenance`, and `qawolf-onboarding` together. Use the [platform guide](skills/qawolf/references/platforms.md) for your client. A skill or instruction file does not imply a working MCP connection; follow the matching setup and verify `whoami`.

## Skills

- **Flow Outline** (`qawolf-flow-outline`) handles every request to create a flow, including finishing a draft and covering a pull request. Your coding agent explores through runner computer use, finds context independently, and uses the ask-user tool for gaps. It presents Arrange, Act, Assert outlines for approval, sends approved outlines through `agent_send`, and monitors creation.
- **Flow Maintenance** (`qawolf-flow-maintenance`) repairs a flow that already exists and has started failing. It reads the recorded run and diagnosis, then hands the fix to `agent_send` without launching a runner.
- **Onboarding** (`qawolf-onboarding`) chooses the best first flow and invokes Flow Outline. A request that already names the new flow goes directly to Flow Outline.
- **QA Wolf** (`qawolf`) supplies shared connection and safety guidance, plus existing-test operations.

Exploration requires a bound workspace. Your new-flow or onboarding request covers billed browser use and routine staging exploration without a separate permission prompt. Your coding agent displays the full AAA before asking for approval, then shares the session URL before monitoring. It continues silently when status is unchanged and verifies publication and the approved draft or active readiness before reporting completion.

## Try it

- "Onboard this app to QA Wolf and find the best first flow."
- "Create a QA Wolf flow for checkout."
- "Run the smoke-tagged QA Wolf flows and summarize what failed."
- "Open a QA Wolf browser and reproduce the login bug."

A cloud browser bills while its runner exists. The skill instructs the agent to terminate the runner when the work ends.

## Troubleshooting

- Connection failure or HTTP 404: check the configured URL and [preview status](https://github.com/qawolf/agent-plugins#status). Reinstalling the plugin cannot fix an unavailable service.
- Sign-in never starts and the connection reports HTTP 401: an `Authorization` header is configured somewhere. Claude Code and Codex skip OAuth when one is set. Remove it from your own `qawolf` MCP entry and reconnect.
- Sign-in fails or the session expires: run `claude mcp login plugin:qawolf:qawolf`, or `codex mcp login qawolf`, and complete the browser flow again.
- Browser-tool authorization error: the connection reaches several workspaces, so it is not bound to one. Call `whoami`, then pass `workspaceId` for the workspace you want, or use a team API key already bound to it.
- Missing agent tools: coverage requests require both `agent_send` and `agent_get`. Contact QA Wolf support if either is unavailable.

Use the [platform guide](skills/qawolf/references/platforms.md) for client-specific connection settings. Never send a QA Wolf API key or OAuth token to an untrusted endpoint.

Report plugin problems through [GitHub issues](https://github.com/qawolf/agent-plugins/issues). Do not include API keys, passwords, or customer test data in public reports.

## Privacy and terms

The plugin sends tool arguments to QA Wolf and returns the requested API results to your coding agent. Depending on the tools used, this can include test data, environment variables, and browser screenshots. Review the requested actions before approving them.

- [QA Wolf privacy policy](https://www.qawolf.com/legal/privacy-policy)
- [QA Wolf terms](https://www.qawolf.com/legal/terms)
- [QA Wolf documentation](https://docs.qawolf.com)
