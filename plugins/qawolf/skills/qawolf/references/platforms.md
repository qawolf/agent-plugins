# Platform setup

QA Wolf uses one shared skill across coding agents. A skill or rule supplies instructions; an MCP connection supplies tools. Installing one does not necessarily install the other.

The distribution follows the thin-adapter approach used by [Ponytail](https://github.com/DietrichGebert/ponytail). The instructions below distinguish native plugins, separately configured MCP clients, and guidance-only hosts. Direct installation is not approval in a provider's official directory.

## Authentication and verification

The production MCP endpoint is `https://app.qawolf.com/api/mcp`. It must be deployed before a client can connect. The current preview uses `Authorization: Bearer <team-api-key>`; OAuth sign-in is not implemented by this bundle.

Obtain a team API key from the QA Wolf app. Configure it outside chat, using the client environment or its secure credential input. Environment-based examples use `QAWOLF_API_KEY`. Desktop apps do not necessarily inherit variables exported in a terminal; make the credential available to the process that actually starts the MCP connection. Never commit a key or put it in a prompt, command-line argument, issue, or screenshot.

For staging, deliberately select `https://app.staging.qawolf.app/api/mcp` and a staging credential. Do not reuse a saved production key without confirming its scope. Merge only the `qawolf` server entry into existing MCP configuration; preserve other servers and settings.

Restart the client or reload its MCP connection, then call `whoami`. Confirm the identity and intended workspace. For onboarding, require `agent_send` and `agent_get`. Browser tools currently require a team API key. If the tools are absent, stop and fix setup rather than claiming the connection works.

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

These native plugins load the shared skill and configure MCP automatically. Set `QAWOLF_API_KEY` in the client launch environment before starting a new session. The same Codex installation is used by its desktop app; restart that app after installation.

Claude supports `QAWOLF_MCP_URL` as an explicit endpoint override. Codex's plugin URL is literal; use a reviewed local copy for staging rather than editing the published defaults.

## GitHub Copilot CLI

Set `QAWOLF_API_KEY` in the client environment, then install:

```bash
copilot plugin marketplace add qawolf/agent-plugins
copilot plugin install qawolf@qawolf
```

The Copilot manifest loads the shared skill and `mcp/copilot.json`. Its `tools: ["*"]` field makes tools available; keep the client's normal action-approval policy. Review an existing server named `qawolf` before installing, because plugin MCP definitions take precedence over user configuration.

Source: [Copilot plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference), [MCP fields](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#mcp-server-configuration).

## Gemini CLI

```bash
gemini extensions install https://github.com/qawolf/agent-plugins
```

Review the extension and enter the key only in Gemini's sensitive setting prompt. The extension declares `QAWOLF_API_KEY` so supported Gemini versions can store it in the system keychain and allow it through extension environment filtering. Do not paste the key into a model prompt or assume an undeclared shell variable survives that filtering.

The public repository exposes `gemini-extension.json` and the complete generated `skills/qawolf/` at its root. A local checkout can also install its nested `plugins/qawolf` directory. The private platform repository itself is not an installable Gemini extension.

Sources: [extensions and settings](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md), [release-root requirements](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/releasing.md).

## Grok Build

Grok accepts the existing Claude-compatible manifest and MCP file.

```bash
grok plugin install 'qawolf/agent-plugins#plugins/qawolf' --trust
grok plugin enable qawolf
```

Review the repository before running the trust-granting install command. Set `QAWOLF_API_KEY` in Grok's launch environment. No Grok-specific copy of the skill is needed.

Sources: [plugins](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/09-plugins.md), [MCP and variable expansion](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/07-mcp-servers.md).

## Devin CLI

Devin's native plugins are in closed beta. The dedicated Devin manifest installs instructions only, instead of falling back to Claude's unverified-for-Devin bearer interpolation.

```bash
devin plugins install 'qawolf/agent-plugins#plugins/qawolf'
devin mcp add -s user qawolf https://app.qawolf.com/api/mcp
```

Configure `headers.Authorization` as a bearer value in the resulting user `~/.config/devin/mcp_config.json`, outside chat. Protect that file and keep it out of source control. No first-party contract was verified for environment interpolation in arbitrary Devin HTTP header values.

Do not use `devin mcp login`; QA Wolf's current endpoint does not implement OAuth. Installing the skill-only manifest is not a working MCP connection.

Sources: [plugins](https://docs.devin.ai/cli/extensibility/plugins/overview), [MCP configuration](https://docs.devin.ai/cli/extensibility/mcp/configuration).

## Qoder CLI

Install from a reviewed public checkout:

```bash
qoder plugins install "$QAWOLF_PLUGIN_ROOT"
```

Here `QAWOLF_PLUGIN_ROOT` is the absolute path to its `plugins/qawolf` directory. The dedicated Qoder manifest installs the shared skill only. No remote marketplace-discovery path has been verified for this repository.

In user `~/.qoder/settings.json`, merge `mcpServers.qawolf` with `type: "http"`, the QA Wolf `url`, and `headers.Authorization`. Enter the bearer credential only in that protected user file. Qoder documents HTTP headers but does not establish variable interpolation specifically in header values; do not assume the Claude syntax works there.

Sources: [plugins](https://docs.qoder.com/cli/plugins.md), [manifest reference](https://docs.qoder.com/cli/plugins-reference.md), [MCP](https://docs.qoder.com/cli/mcp-reference.md).

## Hermes Agent

```bash
hermes plugins install qawolf/agent-plugins/plugins/qawolf --no-enable
hermes plugins enable qawolf
```

Review the native adapter before enabling it. It registers the existing skill and does not start MCP itself. Hermes can prompt securely for the required `QAWOLF_API_KEY` and save it in the active profile. Then merge into the profile's `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  qawolf:
    url: https://app.qawolf.com/api/mcp
    headers:
      Authorization: Bearer ${QAWOLF_API_KEY}
```

Start a new session and explicitly load `skill_view("qawolf:qawolf")`. Plugin skills are namespaced and are not included in Hermes' general available-skills index. Verify QA Wolf tools separately.

Sources: [native plugins and skill registration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/plugins/index.md), [MCP secrets](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/mcp-config-reference.md).

## OpenCode

OpenCode's plugins are executable modules, not a repository bundle for static skills and MCP configuration. No executable OpenCode adapter is needed here.

Install the complete skill at project `.agents/skills/qawolf` or user `~/.config/opencode/skills/qawolf`. Merge this into `opencode.json` or user `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "qawolf": {
      "type": "remote",
      "url": "https://app.qawolf.com/api/mcp",
      "oauth": false,
      "headers": {
        "Authorization": "Bearer {env:QAWOLF_API_KEY}"
      }
    }
  }
}
```

Set the variable in OpenCode's environment. `oauth: false` prevents an OAuth flow that QA Wolf does not support.

Sources: [skills](https://opencode.ai/docs/skills/), [remote MCP](https://opencode.ai/docs/mcp-servers/), [executable plugins](https://opencode.ai/docs/plugins/).

## Pi

```bash
pi install git:github.com/qawolf/agent-plugins
```

Restart Pi or use `/reload`, then invoke `/skill:qawolf`. The package declares the shared skill explicitly and installs no runtime extension or lifecycle hook.

Pi core has [no built-in MCP support](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#philosophy). This install supplies instructions only. Configure the `qawolf` endpoint and bearer credential in an MCP extension you have reviewed and installed separately. Its configuration format depends on that extension; this package does not invent a universal Pi MCP configuration. Verify that the extension exposes QA Wolf tools before trying the skill.

Sources: [Pi packages](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/packages.md), [Pi skills](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md).

## Portable skill files

The public repository exposes `skills/qawolf/SKILL.md` and its complete `references/` directory. They are generated from the canonical `plugins/qawolf/skills/qawolf/` files, not maintained as separate instructions.

For a client with Agent Skills support, install the complete `qawolf` directory into its documented skill location. Keep its `mcp.json` and all references. If a destination already exists, review the differences before updating it. Never replace an application's existing `AGENTS.md`, rules, or MCP configuration wholesale.

## Portable clients with MCP

Install the complete skill using the client's native location below, then configure MCP. These are documented configurations, not a claim that every client has been authenticated in our tests.

For clients supported by the [Agent Skills CLI](https://github.com/vercel-labs/skills), use its interactive target picker:

```bash
npx skills add qawolf/agent-plugins --skill qawolf
```

Review the third-party installer before running it. It installs instructions, not a universal MCP connection. Cline should use its documented `.cline/skills/qawolf` path rather than assuming every installer chooses the right path. CodeWhale and Swival can discover a shared `.agents/skills/qawolf` copy but also offer their own managed locations.

To copy from a reviewed checkout without replacing an existing skill, run this from the application project. Set `QAWOLF_PLUGIN_ROOT` to the checkout's `plugins/qawolf` directory and choose the destination from the table:

```bash
(
  src="$QAWOLF_PLUGIN_ROOT/skills/qawolf"
  dst=".agents/skills/qawolf"
  test -f "$src/SKILL.md" || { printf 'Choose the reviewed plugin directory first\n' >&2; exit 1; }
  test ! -e "$dst" && test ! -L "$dst" || { printf 'Refusing to replace %s\n' "$dst" >&2; exit 1; }
  mkdir -p "$(dirname "$dst")" && cp -R "$src" "$dst"
)
```

| Client                    | Project skill location                               | MCP setup                                                |
| ------------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| Cursor                    | `.agents/skills/qawolf`                              | Merge its environment-backed server entry                |
| Windsurf                  | `.agents/skills/qawolf` or `.windsurf/skills/qawolf` | Merge its environment-backed user config                 |
| Cline                     | `.cline/skills/qawolf`                               | MCP settings UI; environment-backed entry                |
| GitHub Copilot in VS Code | `.github/skills/qawolf` or `.agents/skills/qawolf`   | VS Code MCP profile with a secure input                  |
| Amp                       | `.agents/skills/qawolf`                              | Bundled skill-local MCP config                           |
| Antigravity               | `.agents/skills/qawolf`                              | User config; literal header requires protected storage   |
| Kiro                      | `.kiro/skills/qawolf`                                | Environment-backed user config                           |
| Zed                       | `.agents/skills/qawolf`                              | User settings; literal header requires protected storage |
| CodeWhale                 | `.codewhale/skills/qawolf`                           | CLI supports a bearer-token environment variable         |
| Swival                    | `.swival/skills/qawolf`                              | User config; literal header requires protected storage   |
| OpenClaw                  | Workspace `skills/qawolf`                            | Local skill installer plus environment-backed MCP config |

All JSON below is a merge fragment. Preserve existing settings, server entries, and input definitions. If `qawolf` already exists, review it before changing it.

### Cursor

Merge into `~/.cursor/mcp.json` or project `.cursor/mcp.json`. The key comes from the Cursor process environment.

```json
{
  "mcpServers": {
    "qawolf": {
      "url": "https://app.qawolf.com/api/mcp",
      "headers": {
        "Authorization": "Bearer ${env:QAWOLF_API_KEY}"
      }
    }
  }
}
```

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

Sources: [skills](https://docs.cline.bot/customization/skills), [MCP](https://docs.cline.bot/mcp/configuring-mcp-servers), [environment expansion](https://github.com/cline/cline/blob/main/apps/vscode/src/utils/envExpansion.ts).

### GitHub Copilot in IDEs

For local VS Code, merge this into your user MCP profile or `.vscode/mcp.json`. VS Code prompts for the key and stores the answer securely.

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "qawolf-api-key",
      "description": "QA Wolf team API key",
      "password": true
    }
  ],
  "servers": {
    "qawolf": {
      "type": "http",
      "url": "https://app.qawolf.com/api/mcp",
      "headers": {
        "Authorization": "Bearer ${input:qawolf-api-key}"
      }
    }
  }
}
```

This interactive-input configuration is not forwarded to VS Code's remote Agent Host. Set up that remote process separately rather than assuming it inherits the local credential.

Copilot in JetBrains uses `servers.qawolf.requestInit.headers`, not VS Code's `headers`. Use Copilot Chat > Configure your MCP server and keep the credential in its user-managed file. Visual Studio has a separate Configure MCP server dialog. Use the remote HTTP endpoint and bearer header there. Organization policy may disable MCP in any of these clients.

Where an IDE does not discover skills, append the QA Wolf guidance to its existing repository instructions and point it to the complete installed skill. Do not replace `.github/copilot-instructions.md`.

Sources: [VS Code skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills), [VS Code MCP schema](https://code.visualstudio.com/docs/agents/reference/mcp-configuration), [Copilot MCP by IDE](https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-chat-with-mcp).

### Amp

Install the complete skill and set `QAWOLF_API_KEY` in Amp's environment. The bundled sibling `mcp.json` defines the QA Wolf HTTP server with an environment-backed bearer header. Amp connects when it discovers the skill and exposes its tools when the skill loads.

A directly configured server of the same name takes precedence. Review existing configuration instead of adding a duplicate or assuming the bundled settings override it.

Sources: [skills and skill-local MCP](https://ampcode.com/docs/customize/skills), [MCP configuration](https://ampcode.com/docs/customize/mcp).

### Antigravity

Use the documented skill and MCP setup here. Reuse of Gemini's extension installer by an `agy` binary has not been verified for this package.

Install the skill at `.agents/skills/qawolf`. Merge a `mcpServers.qawolf` entry into user `~/.gemini/config/mcp_config.json`, using `serverUrl` and an `Authorization` header.

The verified documentation shows a literal bearer value, not environment interpolation. Enter it outside chat in the user configuration and restrict file permissions. Do not place it in workspace `.agents/mcp_config.json` or assume an undocumented placeholder expands. Omitting the header can trigger OAuth, which this QA Wolf preview does not provide.

Sources: [skills](https://antigravity.google/docs/skills), [MCP](https://antigravity.google/docs/mcp).

### Kiro

Merge into `~/.kiro/settings/mcp.json`. Approve access to `QAWOLF_API_KEY` when Kiro requests it.

```json
{
  "mcpServers": {
    "qawolf": {
      "url": "https://app.qawolf.com/api/mcp",
      "headers": {
        "Authorization": "Bearer ${QAWOLF_API_KEY}"
      }
    }
  }
}
```

Sources: [skills](https://kiro.dev/docs/skills/), [MCP configuration](https://kiro.dev/docs/mcp/configuration.md).

### Zed

Install the skill at `.agents/skills/qawolf`. Add a remote server under Settings > AI > MCP Servers. Zed stores it under `context_servers.qawolf`, with `url` and `headers.Authorization`.

The verified remote-header documentation does not show secret interpolation. Enter the bearer value only in protected user settings, not project settings. Do not omit the header and expect OAuth to work with the current QA Wolf preview.

Sources: [skills](https://zed.dev/docs/ai/skills), [MCP](https://zed.dev/docs/ai/mcp).

### CodeWhale

Install the skill at `.codewhale/skills/qawolf`, then run:

```bash
codewhale mcp add qawolf \
  --url https://app.qawolf.com/api/mcp \
  --bearer-token-env-var QAWOLF_API_KEY
codewhale mcp reload
codewhale mcp validate
codewhale mcp tools qawolf
```

The default MCP configuration is `~/.codewhale/mcp.json`. The command names an environment variable; it does not contain the secret.

Sources: [skills](https://github.com/Hmbown/Codewhale/blob/main/docs/SKILLS.md), [MCP](https://github.com/Hmbown/Codewhale/blob/main/docs/MCP.md).

### Swival

Install the skill at `.swival/skills/qawolf`, or use its verified shared `.agents/skills/qawolf` location. Its MCP config supports `type = "http"`, `url`, and `headers` under `mcp_servers.qawolf`.

No environment interpolation was verified for remote headers. Enter the bearer value in user-global `~/.config/swival/config.toml` or a private mode-0600 JSON file selected with `--mcp-config`. Do not put it in project `swival.toml` or commit the credential file.

Sources: [skills](https://github.com/Swival/swival/blob/master/docs.md/skills.md), [MCP](https://github.com/Swival/swival/blob/master/docs.md/mcp.md).

### OpenClaw

From a reviewed checkout:

```bash
openclaw skills install "$QAWOLF_PLUGIN_ROOT/skills/qawolf" --as qawolf
openclaw mcp set qawolf \
  '{"url":"https://app.qawolf.com/api/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer ${QAWOLF_API_KEY}"}}'
openclaw mcp doctor qawolf --probe
```

Single quotes preserve the environment placeholder while writing the config. Do not set `auth: "oauth"`: that mode ignores the static Authorization header. No QA Wolf ClawHub listing is claimed by this repository; do not install an unrelated package by name.

Sources: [skills](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md), [MCP CLI](https://github.com/openclaw/openclaw/blob/main/docs/cli/mcp.md), [environment substitution](https://github.com/openclaw/openclaw/blob/main/docs/gateway/configuration.md#environment-variables).

## Guidance-only clients

These adapters can load instructions but do not establish a verified QA Wolf tool connection.

| Client                         | How to load guidance                                                                  | Limitation                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| JetBrains Junie                | Append to the existing `AGENTS.md` or `.junie/AGENTS.md`, or select a Guidelines Path | A current custom remote MCP/bearer contract was not verified for Junie; JetBrains AI Assistant is a different product |
| Jules                          | Append a QA Wolf section to the existing root `AGENTS.md`                             | Its documented MCP picker is curated and does not accept an arbitrary QA Wolf endpoint                                |
| Aider                          | Read the skill and its references with `--read` or an additive `read` config          | No native MCP client is documented; a separate reviewed runtime bridge would be required                              |
| Other instruction-aware agents | Append the supplied QA Wolf guidance and point to the installed skill                 | Verify native MCP support independently                                                                               |

The repository's `AGENTS.md` is a small fallback section, not a replacement for a customer's instructions. Copy or append only the QA Wolf section and retain a usable path to the complete skill. These clients must stop rather than simulate `agent_send` or invent successful test results.

For Aider, load the files without replacing existing context:

```bash
aider \
  --read "$QAWOLF_PLUGIN_ROOT/skills/qawolf/SKILL.md" \
  --read "$QAWOLF_PLUGIN_ROOT/skills/qawolf/references/onboarding.md" \
  --read "$QAWOLF_PLUGIN_ROOT/skills/qawolf/references/platforms.md"
```

Sources: [Junie guidance](https://github.com/JetBrains/junie-guidelines#how-to-use-the-guidelines-in-junie), [Jules MCP scope](https://jules.google/docs/changelog/#mcp-support-comes-to-jules), [Aider conventions](https://aider.chat/docs/usage/conventions.html), [Aider MCP request](https://github.com/Aider-AI/aider/issues/2525).

## Updates and removal

Update through the same client's marketplace, extension manager, or skill installer. For copied files, review and replace only the owned `qawolf` directory. Remove only that directory, its QA Wolf instruction section, and the `qawolf` MCP entry; preserve other skills, settings, and credentials.

Repository updates are not an official-directory submission, npm publication, or ClawHub publication.
