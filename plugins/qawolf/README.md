# QA Wolf plugin

Use QA Wolf from your coding agent to request test coverage, run flows, inspect results, and drive a cloud browser. See [platform setup](skills/qawolf/references/platforms.md) for native plugins, portable skills, MCP configuration, and guidance-only limitations.

This is a preview distributed through the [QA Wolf plugin repository](https://github.com/qawolf/agent-plugins). It is not yet listed in the providers' official directories. The plugin uses a team API key while OAuth support is pending.

## Connect to QA Wolf

QA Wolf clients connect to `https://app.qawolf.com/api/mcp`. Installing the plugin does not authenticate your connection. Check the [preview status](https://github.com/qawolf/agent-plugins#status) before use.

Get a team API key from the QA Wolf app. Set `QAWOLF_API_KEY` in the environment that launches your client. Do not commit the key or paste it into a chat, issue, or screenshot.

Use a secure client credential prompt or set the key in the launch environment without putting its value in shell history. Client-specific configuration is documented in [platform setup](skills/qawolf/references/platforms.md).

Team API keys support browser tools. Organization and user credentials do not currently have access to those tools.

## Install in Claude Code

Start Claude Code from the terminal where you set `QAWOLF_API_KEY`. Then run:

```text
/plugin marketplace add qawolf/agent-plugins
/plugin install qawolf@qawolf
```

Start a new session after installation. Ask Claude to call `whoami` to verify the connection and account.

## Install in Codex

From the terminal where you set `QAWOLF_API_KEY`, run:

```bash
codex plugin marketplace add qawolf/agent-plugins
codex plugin add qawolf@qawolf
```

Start a new Codex session. Ask Codex to call `whoami` to verify the connection and account.

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
- Missing or rejected credential: check `QAWOLF_API_KEY` in the client process and restart the client after changing it.
- Browser-tool authorization error: use a team API key with access to the target workspace.
- Missing agent tools: coverage requests require both `agent_send` and `agent_get`. Contact QA Wolf support if either is unavailable.

Use the [platform guide](skills/qawolf/references/platforms.md) for client-specific connection settings. Never send a QA Wolf API key to an untrusted endpoint.

Report plugin problems through [GitHub issues](https://github.com/qawolf/agent-plugins/issues). Do not include API keys, passwords, or customer test data in public reports.

## Privacy and terms

The plugin sends tool arguments to QA Wolf and returns the requested API results to your coding agent. Depending on the tools used, this can include test data, environment variables, and browser screenshots. Review the requested actions before approving them.

- [QA Wolf privacy policy](https://www.qawolf.com/legal/privacy-policy)
- [QA Wolf terms](https://www.qawolf.com/legal/terms)
- [QA Wolf documentation](https://docs.qawolf.com)
