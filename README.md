# QA Wolf agent plugins

Use QA Wolf from coding agents to request test coverage, run flows, inspect results, and drive a cloud browser. One shared skill supplies the workflow; client adapters and MCP settings supply the tools.

## Status

This is a preview, not an approved listing in the providers' official directories. Clients connect to `https://app.qawolf.com/api/mcp` and sign in with OAuth. Installing the plugin does not authenticate your connection; the client opens a browser on the first connection.

See the [platform setup guide](plugins/qawolf/skills/qawolf/references/platforms.md) for native plugins, separately configured MCP clients, and guidance-only limitations. Do not assume that an instruction file exposes QA Wolf tools.

## Install

Install the plugin for your client, start a fresh session, and approve the browser sign-in. No API key is needed.

Where a browser sign-in cannot happen, such as CI or a container, use the API key fallback in the [platform setup guide](plugins/qawolf/skills/qawolf/references/platforms.md). Configure a key outside chat and keep it out of shell history, source control, prompts, and public issues.

### Claude Code

```text
/plugin marketplace add qawolf/agent-plugins
/plugin install qawolf@qawolf
```

### Codex

```bash
codex plugin marketplace add qawolf/agent-plugins
codex plugin add qawolf@qawolf
```

### GitHub Copilot CLI

```bash
copilot plugin marketplace add qawolf/agent-plugins
copilot plugin install qawolf@qawolf
```

### Gemini CLI

```bash
gemini extensions install https://github.com/qawolf/agent-plugins
```

Then run `/mcp auth qawolf` to sign in.

### Pi

```bash
pi install git:github.com/qawolf/agent-plugins
```

This installs the skill, not an MCP bridge. Pi users need a separately reviewed MCP extension configured for QA Wolf.

### Other Agent Skills clients

Review the third-party installer before running it, then select your client.

```bash
npx skills add qawolf/agent-plugins --skill qawolf
```

MCP setup is separate unless the client reads a bundled MCP adapter. Amp reads the skill's `mcp.json`; other clients should follow the [platform guide](plugins/qawolf/skills/qawolf/references/platforms.md). That guide also covers native installs for Grok, Devin, Qoder, and Hermes, plus manual MCP setup and clients without a verified QA Wolf tool connection.

Restart the client or start a fresh session, then call `whoami` and confirm the account and workspace. For onboarding, require both `agent_send` and `agent_get`. Share the returned session URL; acceptance does not mean the flow is finished. Browser runners bill while they exist, so terminate them when work ends.

If your client uses `AGENTS.md`, append its QA Wolf section rather than replacing your project's existing instructions.

## Try it

- "Ask QA Wolf to cover the checkout journey in this repository."
- "Run the smoke-tagged QA Wolf flows and summarize what failed."
- "Open a QA Wolf browser and reproduce the login bug."

See the [plugin guide](plugins/qawolf/README.md) for authentication requirements and troubleshooting.

## Support and policies

- [Report a plugin issue](https://github.com/qawolf/agent-plugins/issues)
- [QA Wolf documentation](https://docs.qawolf.com)
- [Privacy policy](https://www.qawolf.com/legal/privacy-policy)
- [Terms](https://www.qawolf.com/legal/terms)

Review requested actions before approving them. Tool arguments and results can include test data, environment values, and browser screenshots. Never include credentials or customer test data in public reports.
