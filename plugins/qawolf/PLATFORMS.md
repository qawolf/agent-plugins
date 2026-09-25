# Platform setup

The QA Wolf MCP server supplies the tools and the skills. `skill_list` names the skills and `skill_get` reads one, so a client needs only the MCP connection. These configurations follow client documentation, not authenticated tests of every client.

## Authentication and verification

Connect to `https://app.qawolf.com/api/mcp` and sign in with OAuth. Configure the server with no `Authorization` header. The client discovers QA Wolf's authorization server at `https://signin.qawolf.com`, registers itself, and signs you in.

Clients raise the sign-in in one of two ways. Codex offers it inside the conversation the first time it calls a QA Wolf tool. The ChatGPT app, Claude Code, Claude Desktop, Gemini CLI, and Copilot CLI sign in when the server is added or on first connection, or take an explicit auth command, noted with each client below.

QA Wolf accepts only OAuth, so a client that cannot complete a sign-in cannot connect. A configured `Authorization` header switches OAuth off in several clients, so leave it out.

OAuth signs you in as a QA Wolf user, and the connection reaches every workspace you are a member of, across all of your organizations. `whoami` lists them, each with the organization that owns it. When there is exactly one, the connection binds to it and tools stop asking for `workspaceId`. When there are several it stays unbound, so tools that accept `workspaceId` need it, and a browser tool binds to the workspace you name on the call.

A QA Wolf admin reaches every workspace, including those in organizations they are not a member of. `whoami` lists them all, and reports `canActOnAnyWorkspace`. Demo and sandbox workspaces appear only when the admin belongs to them.

For staging, use `https://app.staging.qawolf.app/api/mcp`. OAuth works there too.

### Verify the connection

All config examples are merge fragments. Preserve existing servers, settings, and inputs; review any existing `qawolf` entry before changing it.

Restart or reload MCP, complete any sign-in prompt, then call `whoami` to confirm identity and workspace. Onboarding needs `agent_send` and `agent_get`. Stop if sign-in cannot be completed.

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

Both plugins install the MCP config, and both sign in with OAuth. Claude Code asks on connection: approve the sign-in it raises, or open `/mcp`, select QA Wolf, and choose Authenticate. Codex offers the sign-in inside the conversation the first time it calls a QA Wolf tool; Codex desktop uses the same installation, and needs a restart after it.

When Claude Code needs sign-in, direct the user to its native `/mcp` controls rather than calling the conversational `authenticate` tool: "First, connect your account. Open `/mcp`, select QA Wolf, and choose Authenticate. Follow the browser sign-in, then return here."

Let the client handle the browser callback and token storage. If the browser does not open, use the link in its authentication UI. If the redirect fails, paste the callback URL only into the client's dedicated authentication prompt, never ordinary chat. Confirm the connection with `whoami` before continuing onboarding.

To sign in by hand, Claude Code needs the plugin-scoped server name, `claude mcp login plugin:qawolf:qawolf`. The bare name does not resolve for a plugin server. Codex uses `codex mcp login qawolf`. Both have a matching `logout`.

Claude accepts `QAWOLF_MCP_URL` overrides. Codex uses a literal URL; use a reviewed local copy for staging.

## ChatGPT app

ChatGPT does not take MCP servers from an installed plugin, so add QA Wolf as a connector once. Turn on developer mode in settings, then add an MCP server with the URL `https://app.qawolf.com/api/mcp` and no header. ChatGPT authorizes it during setup. Add it on the web if the desktop app offers no way to create one, since the app uses the same connector.

Then ask QA Wolf for something in a new chat. On a Business or Enterprise workspace an administrator can publish the same URL once for every member, which replaces the setup above.

Installing the plugin still gives Codex the tools. Its starter prompt, "Verify my QA Wolf connection and workspace", calls `whoami` and reports the workspaces you can act on.

## Claude Desktop

Add QA Wolf as a custom connector with the URL `https://app.qawolf.com/api/mcp` and no header, then authorize it. Claude asks on connection.

## GitHub Copilot CLI

```bash
copilot plugin marketplace add qawolf/agent-plugins
copilot plugin install qawolf@qawolf
```

The plugin loads the MCP config, then signs in with OAuth. Use `/mcp auth` in a session to authenticate or switch accounts.

Requires Copilot CLI 1.0.64 or later. Before that release, MCP servers declared by a plugin never raised an OAuth prompt, so the connection fails silently. On an older build, configure the server by hand in `~/.copilot/mcp-config.json`.

`tools: ["*"]` exposes tools without granting automatic action approval. Plugin servers override same-name user entries; review any existing `qawolf` server first.

Source: [Copilot plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference), [MCP fields](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#mcp-server-configuration).

## Gemini CLI

```bash
gemini extensions install https://github.com/qawolf/agent-plugins
```

Review the extension. Gemini signs in on the first connection; `/mcp auth qawolf` starts it by hand.

Git installation uses the public root manifest. Local installs can use `plugins/qawolf`. The private platform repository is not installable.

Sources: [extensions and settings](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md), [release-root requirements](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/releasing.md).

## Google Antigravity CLI

```bash
agy plugin install https://github.com/qawolf/agent-plugins
```

Then run `/mcp auth qawolf` to sign in. Call `whoami` to confirm your account and workspace before using QA Wolf tools. Installation alone does not authenticate.

Sources: [skills](https://antigravity.google/docs/skills), [MCP](https://antigravity.google/docs/mcp).

## Grok Build

Grok accepts the existing Claude-compatible manifest and MCP file.

```bash
grok plugin install 'qawolf/agent-plugins#plugins/qawolf' --trust
grok plugin enable qawolf
```

Review the repository before granting trust. Grok reads the Claude MCP file, so it connects with no `Authorization` header and signs in with OAuth. Grok's own OAuth handling is unverified.

Sources: [plugins](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/09-plugins.md), [MCP and variable expansion](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/07-mcp-servers.md).

## Devin CLI

Devin plugins are in closed beta. The manifest carries plugin metadata only, so add the MCP server by hand.

```bash
devin plugins install 'qawolf/agent-plugins#plugins/qawolf'
devin mcp add -s user qawolf https://app.qawolf.com/api/mcp
```

Sign in with `devin mcp login qawolf`.

Sources: [plugins](https://docs.devin.ai/cli/extensibility/plugins/overview), [MCP configuration](https://docs.devin.ai/cli/extensibility/mcp/configuration).

## Qoder CLI

Install from a reviewed public checkout:

```bash
qoder plugins install "$QAWOLF_PLUGIN_ROOT"
```

Set `QAWOLF_PLUGIN_ROOT` to the absolute `plugins/qawolf` path. The manifest carries plugin metadata only; remote marketplace discovery is unverified.

In protected user `~/.qoder/settings.json`, add `mcpServers.qawolf` with `type: "http"` and the QA Wolf `url`, and no `Authorization` header, so Qoder can sign in with OAuth. Qoder's OAuth support is unverified.

Sources: [plugins](https://docs.qoder.com/cli/plugins.md), [manifest reference](https://docs.qoder.com/cli/plugins-reference.md), [MCP](https://docs.qoder.com/cli/mcp-reference.md).

## Hermes Agent

No plugin is needed. Merge the server into the active profile's `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  qawolf:
    url: https://app.qawolf.com/api/mcp
```

Hermes' OAuth support is unverified. Reload MCP or complete Hermes' own sign-in, then call `whoami` to verify the tools.

Sources: [MCP configuration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/mcp-config-reference.md).

## OpenCode

No plugin is needed. Merge into `opencode.json` or user `~/.config/opencode/opencode.json`:

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

Pi has [no built-in MCP support](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#philosophy). Install a reviewed MCP extension, configure the endpoint in its format, and verify QA Wolf tools before use. Use an extension that handles MCP OAuth.

## Portable clients with MCP

Configure the QA Wolf MCP server in the client. The server supplies the skills, so no skill files are installed.

| Client                    | MCP setup                                       |
| ------------------------- | ----------------------------------------------- |
| Cursor                    | OAuth sign-in from Tools and Integrations       |
| Windsurf                  | OAuth sign-in; unverified                       |
| Cline                     | OAuth sign-in; unverified for this transport    |
| GitHub Copilot in VS Code | OAuth sign-in; no secure input needed           |
| Amp                       | OAuth sign-in from `amp.mcpServers`; unverified |
| Kiro                      | OAuth sign-in with `/mcp auth`                  |
| Zed                       | OAuth sign-in when no header is set             |
| CodeWhale                 | OAuth sign-in; unverified                       |
| Swival                    | OAuth sign-in; unverified                       |
| OpenClaw                  | OAuth MCP config                                |

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
      "serverUrl": "https://app.qawolf.com/api/mcp"
    }
  }
}
```

Windsurf documents OAuth support for each transport but gives no configuration or sign-in detail, so its sign-in is unverified.

Sources: [skills](https://docs.windsurf.com/windsurf/cascade/skills), [MCP](https://docs.windsurf.com/windsurf/cascade/mcp).

### Cline

Open MCP Servers > Configure and merge this entry. The Cline CLI uses `~/.cline/mcp.json`. Do not enable automatic approval of all QA Wolf tools.

```json
{
  "mcpServers": {
    "qawolf": {
      "type": "streamableHttp",
      "url": "https://app.qawolf.com/api/mcp",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Cline surfaces OAuth on a 401 for SSE servers from 4.1.7 on, but that path is unverified for the `streamableHttp` transport used here.

Sources: [skills](https://docs.cline.bot/customization/skills), [MCP](https://docs.cline.bot/mcp/configuring-mcp-servers).

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

Remote Agent Host cannot run an interactive sign-in, so it cannot connect.

In JetBrains, use Copilot Chat > Configure your MCP server. Visual Studio has its own Configure MCP server dialog. OAuth support in those IDEs is unverified. Organization policy may disable MCP.

If the IDE needs instructions, append the QA Wolf section from `AGENTS.md` to existing instructions. Preserve `.github/copilot-instructions.md`.

Sources: [VS Code skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills), [VS Code MCP schema](https://code.visualstudio.com/docs/agents/reference/mcp-configuration), [Copilot MCP by IDE](https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-chat-with-mcp).

### Amp

Configure the QA Wolf server in `amp.mcpServers` with the URL and no header. Amp documents automatic OAuth for servers in that config, and `amp mcp remote login` covers only servers stored with ampcode.com.

Sources: [skills and skill-local MCP](https://ampcode.com/docs/customize/skills), [MCP configuration](https://ampcode.com/docs/customize/mcp).

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

Run:

```bash
codewhale mcp add qawolf --url https://app.qawolf.com/api/mcp
codewhale mcp reload
codewhale mcp validate
codewhale mcp tools qawolf
```

The default config is `~/.codewhale/mcp.json`. CodeWhale's OAuth support is unverified.

Sources: [skills](https://github.com/Hmbown/Codewhale/blob/main/docs/SKILLS.md), [MCP](https://github.com/Hmbown/Codewhale/blob/main/docs/MCP.md).

### Swival

Configure `mcp_servers.qawolf` with `type = "http"` and `url`.

Swival's OAuth support is unverified.

Sources: [skills](https://github.com/Swival/swival/blob/master/docs.md/skills.md), [MCP](https://github.com/Swival/swival/blob/master/docs.md/mcp.md).

### OpenClaw

From a reviewed checkout:

```bash
openclaw mcp set qawolf \
  '{"url":"https://app.qawolf.com/api/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp doctor qawolf --probe
```

OpenClaw's OAuth support is unverified.

There is no claimed QA Wolf ClawHub listing; do not install an unrelated package by name.

Sources: [skills](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md), [MCP CLI](https://github.com/openclaw/openclaw/blob/main/docs/cli/mcp.md).

## Guidance-only clients

These adapters can load instructions but do not establish a verified QA Wolf tool connection.

| Client                         | How to load guidance                                                                  | Limitation                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| JetBrains Junie                | Append to the existing `AGENTS.md` or `.junie/AGENTS.md`, or select a Guidelines Path | A current custom remote MCP/bearer contract was not verified for Junie; JetBrains AI Assistant is a different product |
| Jules                          | Append a QA Wolf section to the existing root `AGENTS.md`                             | Its documented MCP picker is curated and does not accept an arbitrary QA Wolf endpoint                                |
| Aider                          | Append the QA Wolf section to a file that `--read` or an additive `read` config loads | No native MCP client is documented; a separate reviewed runtime bridge would be required                              |
| Other instruction-aware agents | Append the supplied QA Wolf guidance                                                  | Verify native MCP support independently                                                                               |

Append only the QA Wolf section from the supplied `AGENTS.md`. Preserve existing instructions. Without tools, stop; never simulate `agent_send` or invent test results.

Sources: [Junie guidance](https://github.com/JetBrains/junie-guidelines#how-to-use-the-guidelines-in-junie), [Jules MCP scope](https://jules.google/docs/changelog/#mcp-support-comes-to-jules), [Aider conventions](https://aider.chat/docs/usage/conventions.html), [Aider MCP request](https://github.com/Aider-AI/aider/issues/2525).

## Updates and removal

Use the original installer to update. The agent reads each skill from the server on every call, so a skill change needs no update on your side. To uninstall, remove the plugin, the QA Wolf instruction section, and its MCP entry. Preserve other settings and credentials.
