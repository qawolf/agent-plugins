# QA Wolf plugin

Use QA Wolf from Claude Code or Codex to request test coverage, run flows, inspect results, and drive a cloud browser.

This is a preview distributed through the [QA Wolf plugin repository](https://github.com/qawolf/agent-plugins). It is not yet listed in the providers' official directories. The plugin uses a team API key while OAuth support is pending.

## Connect to QA Wolf

Both clients connect to `https://app.qawolf.com/api/mcp`. The endpoint must be available in the deployed QA Wolf backend. Installing the plugin does not deploy the server.

Get a team API key from the QA Wolf app. Set `QAWOLF_API_KEY` in the environment that launches your client. Do not commit the key or paste it into a chat, issue, or screenshot.

```bash
export QAWOLF_API_KEY='your-team-api-key'
```

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

## Try it

- "Ask QA Wolf to cover the checkout journey in this repository."
- "Run the smoke-tagged QA Wolf flows and summarize what failed."
- "Open a QA Wolf browser and reproduce the login bug."

Coverage requests use `agent_send` and `agent_get`. The skill checks that the connected server exposes both tools before using them. If either is absent, that deployment does not yet support coverage requests.

A cloud browser bills while its runner exists. The skill instructs the agent to terminate the runner when the work ends.

## Troubleshooting

- Connection failure or HTTP 404: the configured endpoint is unavailable. Check the URL and server deployment; installing the plugin cannot fix a missing route.
- Missing or rejected credential: check `QAWOLF_API_KEY` in the client process and restart the client after changing it.
- Browser-tool authorization error: use a team API key with access to the target workspace.
- Missing agent tools: wait for a deployment that includes them. Other tools can still work.

Claude Code supports a full endpoint override through `QAWOLF_MCP_URL`. For example, local development can use `http://localhost:3000/api/mcp`. Codex uses a literal URL in `mcp/codex.json`; edit a local checkout and reinstall that plugin when testing another deployment. Never send a production key to an untrusted endpoint.

Report plugin problems through [GitHub issues](https://github.com/qawolf/agent-plugins/issues). Do not include API keys, passwords, or customer test data in public reports.

## Privacy and terms

The plugin sends tool arguments to QA Wolf and returns the requested API results to your coding agent. Depending on the tools used, this can include test data, environment variables, and browser screenshots. Review the requested actions before approving them.

- [QA Wolf privacy policy](https://www.qawolf.com/legal/privacy-policy)
- [QA Wolf terms](https://www.qawolf.com/legal/terms)
- [QA Wolf documentation](https://docs.qawolf.com)

## Package layout

Claude Code reads `.claude-plugin/plugin.json`; Codex reads `.codex-plugin/plugin.json`. Both load `skills/qawolf/SKILL.md`.

The manifests point to separate MCP configs. Claude uses an authorization header with `${QAWOLF_API_KEY}` in `mcp/claude.json`. Codex uses `bearer_token_env_var` in `mcp/codex.json`. There is no shared root `.mcp.json` because the clients use different credential formats.
