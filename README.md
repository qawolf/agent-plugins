# QA Wolf agent plugins

Use QA Wolf from coding agents to request test coverage, run flows, inspect results, and drive a cloud browser. One shared skill supplies the workflow; client adapters and MCP settings supply the tools.

## Status

This is an API-key preview, not an approved listing in the providers' official directories. At the 0.1.2 publication check on 2026-09-07, production `/api/mcp` still returned HTTP 404. The assets are published for preview; production use requires the MCP backend deployment. The production MCP endpoint is `https://app.qawolf.com/api/mcp`; installing client files does not deploy that server or authenticate the connection. OAuth support remains pending.

See the [platform setup guide](plugins/qawolf/skills/qawolf/references/platforms.md) for native plugins, separately configured MCP clients, and guidance-only limitations. Do not assume that an instruction file exposes QA Wolf tools.

## Install

Get a team API key from QA Wolf. Configure it outside chat through the client's secure credential input or launch environment, normally as `QAWOLF_API_KEY`. Do not put the key in shell history, source control, a prompt, or a public issue. Desktop clients need the credential in the process that actually starts their MCP connection.

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

Enter the API key only in Gemini's sensitive extension-setting prompt.

### Pi

```bash
pi install git:github.com/qawolf/agent-plugins
```

This installs the skill, not an MCP bridge. Pi users need a separately reviewed MCP extension configured for QA Wolf.

### Other Agent Skills clients

```bash
npx skills add qawolf/agent-plugins --skill qawolf
```

Review the third-party installer and select your client. MCP setup is separate unless the client reads a bundled MCP adapter. Amp reads the skill's `mcp.json`; other clients should follow the [platform guide](plugins/qawolf/skills/qawolf/references/platforms.md). That guide also covers native installs for Grok, Devin, Qoder, and Hermes, plus manual MCP setup and clients without a verified QA Wolf tool connection.

Restart the client or start a fresh session, then call `whoami` and confirm the account and workspace. For onboarding, require both `agent_send` and `agent_get`. Share the returned session URL; acceptance does not mean the flow is finished. Browser runners bill while they exist, so terminate them when work ends.

## Distribution layout

- `plugins/qawolf/` is the canonical client bundle, including the complete shared skill and setup references.
- `skills/qawolf/` is generated from that skill for clients that discover repository-root skills. It is not edited independently.
- Root manifests and catalogs are client entrypoints, not QA Wolf server code.
- `AGENTS.md` supplies a short fallback for instruction-aware clients. Append its QA Wolf section rather than replacing a project's existing instructions.

## Validation

```bash
claude plugin validate ./ --strict
claude plugin validate ./plugins/qawolf --strict
```

Codex can install a checkout with `codex plugin marketplace add ./`, then `codex plugin add qawolf@qawolf`. File and manifest validation is not proof of an authenticated connection in every supported client; verify `whoami` in the client you use.

## Releases

Changes belong in the platform's dedicated agent-plugins package, not in this generated distribution. The independent publishing workflow checks a successful production deployment job and the exact healthy Apex commit before copying approved client files.

Changed bundle or root-adapter content receives one new patch version across versioned client entrypoints. A higher author-declared version takes precedence. Unchanged releases do not create commits. Publishing preserves unrelated repository files and marketplace entries, including this README.

Automation requires the QA Wolf Ops GitHub App installation to include this repository. Manual previews may be published before the corresponding backend release; they do not establish deployment or authentication success.

Updating this repository does not publish to npm, ClawHub, or an official provider directory. Those require separate authorization and publication steps.

## Support and policies

- [Report a plugin issue](https://github.com/qawolf/agent-plugins/issues)
- [QA Wolf documentation](https://docs.qawolf.com)
- [Privacy policy](https://www.qawolf.com/legal/privacy-policy)
- [Terms](https://www.qawolf.com/legal/terms)

Review requested actions before approving them. Tool arguments and results can include test data, environment values, and browser screenshots. Never include credentials or customer test data in public reports.
