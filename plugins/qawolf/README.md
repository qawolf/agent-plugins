# QA Wolf plugin

Use QA Wolf from your coding agent to request test coverage, run flows, inspect results, and drive a cloud browser. See [platform setup](skills/qawolf/references/platforms.md) for native plugins, portable skills, MCP configuration, and guidance-only limitations.

This is a preview distributed through the [QA Wolf plugin repository](https://github.com/qawolf/agent-plugins). It is not yet listed in the providers' official directories. The plugin signs in with OAuth.

## Connect to QA Wolf

QA Wolf clients connect to `https://app.qawolf.com/api/mcp` and sign in with OAuth. Installing the plugin does not authenticate your connection. Your client opens a browser on the first connection and signs you in through `https://signin.qawolf.com`. Check the [preview status](https://github.com/qawolf/agent-plugins#status) before use.

No API key is needed. Do not add an `Authorization` header to the plugin's MCP entry; in Claude Code and Codex a configured header switches OAuth off and the connection fails with HTTP 401.

Where a browser sign-in cannot happen, such as CI or a container, use the API key fallback described in [platform setup](skills/qawolf/references/platforms.md). Keep any key out of shell history, source control, chats, issues, and screenshots.

Browser tools need a bound workspace. OAuth binds one when your organization has a single QA Wolf workspace; a team API key is always bound to its team.

## Install in Claude Code

```text
/plugin marketplace add qawolf/agent-plugins
/plugin install qawolf@qawolf
```

Start a new session after installation and approve the browser sign-in. To sign in by hand, run `claude mcp login plugin:qawolf:qawolf`; the plugin-scoped name is required, and the bare `qawolf` does not resolve. Then ask Claude to call `whoami` to verify the connection and account.

## Install in Codex

```bash
codex plugin marketplace add qawolf/agent-plugins
codex plugin add qawolf@qawolf
```

Start a new Codex session and approve the browser sign-in, or run `codex mcp login qawolf`. Then ask Codex to call `whoami` to verify the connection and account.

## Other coding agents

The public repository also exposes the complete skill at `skills/qawolf/` and a Pi package entrypoint. Use the [platform guide](skills/qawolf/references/platforms.md) for your client. A skill or instruction file does not imply a working MCP connection; follow the matching setup and verify `whoami`.

## Try it

- "Ask QA Wolf to cover the checkout journey in this repository."
- "Run the smoke-tagged QA Wolf flows and summarize what failed."
- "Open a QA Wolf browser and reproduce the login bug."

Coverage requests use `agent_send` and `agent_get`. The skill checks that both tools are available before using them.

A cloud browser bills while its runner exists. The skill instructs the agent to terminate the runner when the work ends.

## Troubleshooting

- Connection failure or HTTP 404: check the configured URL and [preview status](https://github.com/qawolf/agent-plugins#status). Reinstalling the plugin cannot fix an unavailable service.
- Sign-in never starts and the connection reports HTTP 401: an `Authorization` header is configured somewhere. Claude Code and Codex skip OAuth when one is set. Remove it from your own `qawolf` MCP entry and reconnect.
- Sign-in fails or the session expires: run `claude mcp login plugin:qawolf:qawolf`, or `codex mcp login qawolf`, and complete the browser flow again.
- Browser-tool authorization error: the connection has no bound workspace. Call `whoami`. If it lists several workspaces, pass `workspaceId` where tools accept it, or use a team API key for the target workspace.
- Missing agent tools: coverage requests require both `agent_send` and `agent_get`. Contact QA Wolf support if either is unavailable.

Use the [platform guide](skills/qawolf/references/platforms.md) for client-specific connection settings. Never send a QA Wolf API key or OAuth token to an untrusted endpoint.

Report plugin problems through [GitHub issues](https://github.com/qawolf/agent-plugins/issues). Do not include API keys, passwords, or customer test data in public reports.

## Privacy and terms

The plugin sends tool arguments to QA Wolf and returns the requested API results to your coding agent. Depending on the tools used, this can include test data, environment variables, and browser screenshots. Review the requested actions before approving them.

- [QA Wolf privacy policy](https://www.qawolf.com/legal/privacy-policy)
- [QA Wolf terms](https://www.qawolf.com/legal/terms)
- [QA Wolf documentation](https://docs.qawolf.com)
