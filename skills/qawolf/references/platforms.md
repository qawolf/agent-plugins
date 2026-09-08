# Platform setup

Skills supply instructions; MCP supplies tools. Some clients need separate setup for each. These configurations follow client documentation, not authenticated tests of every client. Direct installation is not official-directory approval.

## Authentication and verification

Connect to `https://app.qawolf.com/api/mcp` and sign in with OAuth. Configure the server with no `Authorization` header. The client discovers QA Wolf's authorization server at `https://signin.qawolf.com`, registers itself, and opens a browser to sign you in. Most clients start this on the first connection. Some need an explicit auth command, noted with each client below.

A configured `Authorization` header switches OAuth off in several clients, so leave it out unless you are using the API key fallback.

OAuth signs you in as a QA Wolf user. If your organization has one workspace, the connection binds to it and tools stop asking for `workspaceId`. If it has several, `whoami` returns the candidates, tools that accept `workspaceId` still need it, and browser tools stay unavailable until a workspace is bound.

### API key fallback

Use a team API key where a browser sign-in cannot happen, such as CI, a container, or a client with no OAuth support. Send it as `Authorization: Bearer <team-api-key>`.

Get a team API key from QA Wolf and configure it outside chat. Examples use `QAWOLF_API_KEY` in the client process environment; desktop apps may not inherit terminal variables. Never put keys in prompts, command-line arguments, issues, screenshots, or source control.

For staging, use `https://app.staging.qawolf.app/api/mcp`. OAuth works there too. If you use a staging API key instead, do not assume a saved production key applies.

### Verify the connection

All config examples are merge fragments. Preserve existing servers, settings, and inputs; review any existing `qawolf` entry before changing it. Keep literal credentials in protected user files, never project files.

Restart or reload MCP, complete any sign-in prompt, then call `whoami` to confirm identity and workspace. Onboarding needs `agent_send` and `agent_get`. Stop if required tools or authentication are missing.

## Claude Code and Codex

Claude Code:

```text
/plugin marketplace add qawolf/agent-plugins
/plugin install qawolf@qawolf
```

Codex:

```bash
codex plugin marketplace add qawolf/agent-plugins
codex plugin add qawolf@qawolf
```

Both plugins install the skill and MCP config, and both sign in with OAuth. Start a fresh session, then approve the browser sign-in when the client asks. Codex desktop uses the same installation; restart it.

To sign in by hand, Claude Code needs the plugin-scoped server name, `claude mcp login plugin:qawolf:qawolf`. The bare name does not resolve for a plugin server. Codex uses `codex mcp login qawolf`. Both have a matching `logout`.

Claude accepts `QAWOLF_MCP_URL` overrides. Codex uses a literal URL; use a reviewed local copy for staging.

## GitHub Copilot CLI

```bash
copilot plugin marketplace add qawolf/agent-plugins
copilot plugin install qawolf@qawolf
```

The plugin loads the skill and MCP config, then signs in with OAuth. Use `/mcp auth` in a session to authenticate or switch accounts.

Requires Copilot CLI 1.0.64 or later. Before that release, MCP servers declared by a plugin never raised an OAuth prompt, so the connection fails silently. On an older build, configure the server by hand in `~/.copilot/mcp-config.json`.

`tools: ["*"]` exposes tools without granting automatic action approval. Plugin servers override same-name user entries; review any existing `qawolf` server first.

Source: [Copilot plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference), [MCP fields](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#mcp-server-configuration).

## Gemini CLI

```bash
gemini extensions install https://github.com/qawolf/agent-plugins
```

Review the extension, then run `/mcp auth qawolf` to sign in. Use the explicit command; Gemini's automatic sign-in on connect does not reach QA Wolf yet, because it probes the endpoint with `HEAD` and QA Wolf answers `405` there instead of the `401` that carries the discovery header.

Git installation uses the public root manifest and skills. Local installs can use `plugins/qawolf`. The private platform repository is not installable.

Sources: [extensions and settings](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md), [release-root requirements](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/releasing.md).

## Grok Build

Grok accepts the existing Claude-compatible manifest and MCP file.

```bash
grok plugin install 'qawolf/agent-plugins#plugins/qawolf' --trust
grok plugin enable qawolf
```

Review the repository before granting trust. Grok reads the Claude MCP file, so it connects with no `Authorization` header and signs in with OAuth. Grok's own OAuth handling is unverified; if no sign-in prompt appears, add the API key fallback header to its config.

Sources: [plugins](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/09-plugins.md), [MCP and variable expansion](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/07-mcp-servers.md).

## Devin CLI

Devin plugins are in closed beta. This manifest installs the skill only.

```bash
devin plugins install 'qawolf/agent-plugins#plugins/qawolf'
devin mcp add -s user qawolf https://app.qawolf.com/api/mcp
```

Sign in with `devin mcp login qawolf`. If Devin does not complete the flow, set a literal bearer value in `headers.Authorization` in protected user `~/.config/devin/mcp_config.json`. Header environment expansion is unverified.

Sources: [plugins](https://docs.devin.ai/cli/extensibility/plugins/overview), [MCP configuration](https://docs.devin.ai/cli/extensibility/mcp/configuration).

## Qoder CLI

Install from a reviewed public checkout:

```bash
qoder plugins install "$QAWOLF_PLUGIN_ROOT"
```

Set `QAWOLF_PLUGIN_ROOT` to the absolute `plugins/qawolf` path. This installs the skill only; remote marketplace discovery is unverified.

In protected user `~/.qoder/settings.json`, add `mcpServers.qawolf` with `type: "http"` and the QA Wolf `url`, and no `Authorization` header, so Qoder can sign in with OAuth. Qoder's OAuth support is unverified. If it never prompts, add a literal bearer value in `headers.Authorization`; header environment expansion is unverified.

Sources: [plugins](https://docs.qoder.com/cli/plugins.md), [manifest reference](https://docs.qoder.com/cli/plugins-reference.md), [MCP](https://docs.qoder.com/cli/mcp-reference.md).

## Hermes Agent

```bash
hermes plugins install qawolf/agent-plugins/plugins/qawolf --no-enable
hermes plugins enable qawolf
```

Review the adapter before enabling it. It registers the skill, not MCP. Merge the server into the active profile's `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  qawolf:
    url: https://app.qawolf.com/api/mcp
```

Hermes' OAuth support is unverified. If it never prompts you to sign in, save `QAWOLF_API_KEY` through Hermes' secure prompt and add the fallback header:

```yaml
mcp_servers:
  qawolf:
    headers:
      Authorization: Bearer ${QAWOLF_API_KEY}
```

Start a new session and call `skill_view("qawolf:qawolf")`; plugin skills are absent from the general skill index. Verify MCP tools separately.

Sources: [native plugins and skill registration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/plugins/index.md), [MCP secrets](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/mcp-config-reference.md).

## OpenCode

No executable plugin is needed. Copy the complete skill to project `.agents/skills/qawolf` or user `~/.config/opencode/skills/qawolf`. Merge into `opencode.json` or user `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "qawolf": {
      "type": "remote",
      "url": "https://app.qawolf.com/api/mcp"
    }
  }
}
```

OpenCode detects the 401, registers a client, and opens a browser. Sign in by hand with `opencode mcp auth qawolf`, and check state with `opencode mcp debug`. Do not set `oauth: true`. That field accepts an object or the literal `false`, and `false` turns the flow off.

Sources: [skills](https://opencode.ai/docs/skills/), [remote MCP](https://opencode.ai/docs/mcp-servers/), [executable plugins](https://opencode.ai/docs/plugins/).

## Pi

```bash
pi install git:github.com/qawolf/agent-plugins
```

Restart or `/reload`, then use `/skill:qawolf`. This installs instructions only, with no extension or hooks.

Pi has [no built-in MCP support](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#philosophy). Install a reviewed MCP extension, configure the endpoint in its format, and verify QA Wolf tools before use. Prefer an extension that handles MCP OAuth. If none is available, supply a team API key as a bearer credential.

Sources: [Pi packages](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/packages.md), [Pi skills](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md).

## Portable skill files

Public `skills/qawolf/` comes from `plugins/qawolf/skills/qawolf/`. Copy the whole directory, including `mcp.json` and references. Review existing files before updating; never replace an application's instructions or configuration wholesale.

## Portable clients with MCP

Install the skill at the location below, then configure MCP. Clients supported by the [Agent Skills CLI](https://github.com/vercel-labs/skills) can use its target picker:

Review the installer first and check its destination, especially Cline's `.cline/skills/qawolf`. CodeWhale and Swival also accept `.agents/skills/qawolf`.

```bash
npx skills add qawolf/agent-plugins --skill qawolf
```

For a manual copy, set `QAWOLF_PLUGIN_ROOT` to a reviewed checkout's `plugins/qawolf` directory. Run from the application project and choose a destination below. This refuses to replace an existing skill:

```bash
(
  src="$QAWOLF_PLUGIN_ROOT/skills/qawolf"
  dst=".agents/skills/qawolf"
  test -f "$src/SKILL.md" || { printf 'Choose the reviewed plugin directory first\n' >&2; exit 1; }
  test ! -e "$dst" && test ! -L "$dst" || { printf 'Refusing to replace %s\n' "$dst" >&2; exit 1; }
  mkdir -p "$(dirname "$dst")" && cp -R "$src" "$dst"
)
```

| Client                    | Project skill location                               | MCP setup                                             |
| ------------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| Cursor                    | `.agents/skills/qawolf`                              | OAuth sign-in from Tools and Integrations             |
| Windsurf                  | `.agents/skills/qawolf` or `.windsurf/skills/qawolf` | API key fallback; OAuth unverified                    |
| Cline                     | `.cline/skills/qawolf`                               | API key fallback; OAuth unverified for this transport |
| GitHub Copilot in VS Code | `.github/skills/qawolf` or `.agents/skills/qawolf`   | OAuth sign-in; no secure input needed                 |
| Amp                       | `.agents/skills/qawolf`                              | Bundled skill-local config; OAuth unverified          |
| Antigravity               | `.agents/skills/qawolf`                              | API key fallback; OAuth unverified                    |
| Kiro                      | `.kiro/skills/qawolf`                                | OAuth sign-in with `/mcp auth`                        |
| Zed                       | `.agents/skills/qawolf`                              | OAuth sign-in when no header is set                   |
| CodeWhale                 | `.codewhale/skills/qawolf`                           | API key fallback; OAuth unverified                    |
| Swival                    | `.swival/skills/qawolf`                              | API key fallback; OAuth unverified                    |
| OpenClaw                  | Workspace `skills/qawolf`                            | Local skill installer plus OAuth MCP config           |

### Cursor

Merge into `~/.cursor/mcp.json` or project `.cursor/mcp.json`.

```json
{
  "mcpServers": {
    "qawolf": {
      "url": "https://app.qawolf.com/api/mcp"
    }
  }
}
```

Sign in from Tools and Integrations, where the server appears with a "Needs login" entry. Cursor does not document whether it starts the flow on its own after a 401. Its redirect URIs are fixed, `https://www.cursor.com/agents/mcp/oauth/callback` for web and `http://localhost:8787/callback` for desktop. Cursor's static `auth` block, with `CLIENT_ID` and `CLIENT_SECRET`, is only for a pre-registered client and is not needed here.

Sources: [skills](https://cursor.com/docs/skills), [MCP](https://cursor.com/docs/mcp).

### Windsurf

Merge into `~/.codeium/windsurf/mcp_config.json`.

```json
{
  "mcpServers": {
    "qawolf": {
      "serverUrl": "https://app.qawolf.com/api/mcp",
      "headers": {
        "Authorization": "Bearer ${env:QAWOLF_API_KEY}"
      }
    }
  }
}
```

Windsurf documents OAuth support for each transport but gives no configuration or sign-in detail, so this keeps the API key fallback. Try removing the header first, and leave it out if a sign-in prompt appears.

Sources: [skills](https://docs.windsurf.com/windsurf/cascade/skills), [MCP](https://docs.windsurf.com/windsurf/cascade/mcp).

### Cline

Open MCP Servers > Configure and merge this entry. The Cline CLI uses `~/.cline/mcp.json`. Do not enable automatic approval of all QA Wolf tools.

```json
{
  "mcpServers": {
    "qawolf": {
      "type": "streamableHttp",
      "url": "https://app.qawolf.com/api/mcp",
      "headers": {
        "Authorization": "Bearer ${env:QAWOLF_API_KEY}"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Cline surfaces OAuth on a 401 for SSE servers from 4.1.7 on, but that path is unverified for the `streamableHttp` transport used here, so this keeps the API key fallback.

Sources: [skills](https://docs.cline.bot/customization/skills), [MCP](https://docs.cline.bot/mcp/configuring-mcp-servers), [environment expansion](https://github.com/cline/cline/blob/main/apps/vscode/src/utils/envExpansion.ts).

### GitHub Copilot in IDEs

For local VS Code, merge this into your user MCP profile or `.vscode/mcp.json`.

```json
{
  "servers": {
    "qawolf": {
      "type": "http",
      "url": "https://app.qawolf.com/api/mcp"
    }
  }
}
```

VS Code registers a client and signs you in through the browser, so no `inputs` entry is needed. Account state lives in the Accounts menu and under Manage Trusted MCP Servers.

Remote Agent Host cannot run an interactive sign-in; configure its credentials separately with the API key fallback.

JetBrains uses `servers.qawolf.requestInit.headers`. Use Copilot Chat > Configure your MCP server and protected user settings. Visual Studio has its own Configure MCP server dialog. OAuth support in those IDEs is unverified; supply the bearer header if no sign-in appears. Organization policy may disable MCP.

If the IDE cannot discover skills, append QA Wolf guidance and the skill path to existing instructions. Preserve `.github/copilot-instructions.md`.

Sources: [VS Code skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills), [VS Code MCP schema](https://code.visualstudio.com/docs/agents/reference/mcp-configuration), [Copilot MCP by IDE](https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-chat-with-mcp).

### Amp

The skill's `mcp.json` configures MCP with no header, so Amp can sign in with OAuth. Amp connects at skill discovery and exposes tools when the skill loads. A same-name directly configured server overrides it; review existing entries.

Amp documents automatic OAuth for servers in its own `amp.mcpServers` config but not for a skill-local `mcp.json`, and `amp mcp remote login` covers only servers stored with ampcode.com. If the skill's server never prompts, move the entry into `amp.mcpServers`, or add the API key fallback header to the skill's `mcp.json`.

Sources: [skills and skill-local MCP](https://ampcode.com/docs/customize/skills), [MCP configuration](https://ampcode.com/docs/customize/mcp).

### Antigravity

Gemini extension installation through `agy` is unverified. Copy the skill to `.agents/skills/qawolf`.

In protected user `~/.gemini/config/mcp_config.json`, add `mcpServers.qawolf` with `serverUrl`. Antigravity's OAuth support is unverified. If it never prompts, add a literal bearer `Authorization` header; header environment expansion is unverified. Do not store the key in workspace `.agents/mcp_config.json`.

Sources: [skills](https://antigravity.google/docs/skills), [MCP](https://antigravity.google/docs/mcp).

### Kiro

Merge into `~/.kiro/settings/mcp.json`.

```json
{
  "mcpServers": {
    "qawolf": {
      "url": "https://app.qawolf.com/api/mcp"
    }
  }
}
```

Kiro runs the browser flow and registers a client when none is configured. Use `/mcp auth` to sign in and `/mcp logout` to clear it.

Sources: [skills](https://kiro.dev/docs/skills/), [MCP configuration](https://kiro.dev/docs/mcp/configuration.md).

### Zed

Add a remote server under Settings > AI > MCP Servers. Use `context_servers.qawolf` with `url` and no `headers`. With no `Authorization` header configured, Zed prompts you to sign in through the standard MCP OAuth flow.

Sources: [skills](https://zed.dev/docs/ai/skills), [MCP](https://zed.dev/docs/ai/mcp).

### CodeWhale

Install the skill at `.codewhale/skills/qawolf`, then run:

```bash
codewhale mcp add qawolf --url https://app.qawolf.com/api/mcp
codewhale mcp reload
codewhale mcp validate
codewhale mcp tools qawolf
```

The default config is `~/.codewhale/mcp.json`. CodeWhale's OAuth support is unverified. If `mcp validate` reports an authentication failure, re-add the server with `--bearer-token-env-var QAWOLF_API_KEY`, which stores the variable name and not its value.

Sources: [skills](https://github.com/Hmbown/Codewhale/blob/main/docs/SKILLS.md), [MCP](https://github.com/Hmbown/Codewhale/blob/main/docs/MCP.md).

### Swival

Use `.swival/skills/qawolf` or `.agents/skills/qawolf`. Configure `mcp_servers.qawolf` with `type = "http"` and `url`.

Swival's OAuth support is unverified. If it never prompts, add `headers` with a literal bearer value. Header environment expansion is unverified. Store that value in user `~/.config/swival/config.toml` or a mode-0600 JSON file selected with `--mcp-config`, never project `swival.toml`.

Sources: [skills](https://github.com/Swival/swival/blob/master/docs.md/skills.md), [MCP](https://github.com/Swival/swival/blob/master/docs.md/mcp.md).

### OpenClaw

From a reviewed checkout:

```bash
openclaw skills install "$QAWOLF_PLUGIN_ROOT/skills/qawolf" --as qawolf
openclaw mcp set qawolf \
  '{"url":"https://app.qawolf.com/api/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp doctor qawolf --probe
```

OpenClaw's OAuth support is unverified. If `mcp doctor` reports an authentication failure, set a static header instead. Single quotes preserve the variable placeholder:

```bash
openclaw mcp set qawolf \
  '{"url":"https://app.qawolf.com/api/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer ${QAWOLF_API_KEY}"}}'
```

There is no claimed QA Wolf ClawHub listing; do not install an unrelated package by name.

Sources: [skills](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md), [MCP CLI](https://github.com/openclaw/openclaw/blob/main/docs/cli/mcp.md), [environment substitution](https://github.com/openclaw/openclaw/blob/main/docs/gateway/configuration.md#environment-variables).

## Guidance-only clients

These adapters can load instructions but do not establish a verified QA Wolf tool connection.

| Client                         | How to load guidance                                                                  | Limitation                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| JetBrains Junie                | Append to the existing `AGENTS.md` or `.junie/AGENTS.md`, or select a Guidelines Path | A current custom remote MCP/bearer contract was not verified for Junie; JetBrains AI Assistant is a different product |
| Jules                          | Append a QA Wolf section to the existing root `AGENTS.md`                             | Its documented MCP picker is curated and does not accept an arbitrary QA Wolf endpoint                                |
| Aider                          | Read the skill and its references with `--read` or an additive `read` config          | No native MCP client is documented; a separate reviewed runtime bridge would be required                              |
| Other instruction-aware agents | Append the supplied QA Wolf guidance and point to the installed skill                 | Verify native MCP support independently                                                                               |

Append only the QA Wolf section from the supplied `AGENTS.md`, with a usable skill path. Preserve existing instructions. Without tools, stop; never simulate `agent_send` or invent test results.

For Aider, load the files without replacing existing context:

```bash
aider \
  --read "$QAWOLF_PLUGIN_ROOT/skills/qawolf/SKILL.md" \
  --read "$QAWOLF_PLUGIN_ROOT/skills/qawolf/references/onboarding.md" \
  --read "$QAWOLF_PLUGIN_ROOT/skills/qawolf/references/platforms.md"
```

Sources: [Junie guidance](https://github.com/JetBrains/junie-guidelines#how-to-use-the-guidelines-in-junie), [Jules MCP scope](https://jules.google/docs/changelog/#mcp-support-comes-to-jules), [Aider conventions](https://aider.chat/docs/usage/conventions.html), [Aider MCP request](https://github.com/Aider-AI/aider/issues/2525).

## Updates and removal

Use the original installer to update. For manual copies, review and replace only `qawolf`. To uninstall, remove its skill directory, instruction section, and MCP entry. Preserve other skills, settings, and credentials.

Repository updates do not publish to official directories, npm, or ClawHub.
