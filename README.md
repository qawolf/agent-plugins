# QA Wolf agent plugins

QA Wolf plugins for Claude Code and Codex. Request test coverage, run flows, inspect results, and use a cloud browser through the QA Wolf MCP endpoint.

## Status

Preview release. This repository supports direct marketplace installation; it is not an approved listing in the providers' official directories. OAuth support and directory-review metadata are still pending.

The plugin points to `https://app.qawolf.com/api/mcp` and requires a compatible server deployment. It currently authenticates with `QAWOLF_API_KEY`, set in the client environment. Do not commit your key or share it in a public issue.

## Install

Get a team API key from the QA Wolf app and set it in the terminal that launches your client:

```bash
export QAWOLF_API_KEY='your-team-api-key'
```

### Claude Code

Start Claude Code, then run:

```text
/plugin marketplace add qawolf/agent-plugins
/plugin install qawolf@qawolf
```

### Codex

```bash
codex plugin marketplace add qawolf/agent-plugins
codex plugin add qawolf@qawolf
```

Start a new session after installation. Ask your agent to call `whoami` to verify the connection and account.

See the [plugin guide](plugins/qawolf/README.md) for workflows, authentication, and troubleshooting. Browser runners bill while they exist; terminate them when the work ends.

## Validate a checkout

```bash
claude plugin validate ./ --strict
claude plugin validate ./plugins/qawolf --strict
```

Codex can load this checkout with `codex plugin marketplace add ./`. Inspect it with `codex plugin list --marketplace qawolf --available --json`.

Both manifests use the same version. Bump the plugin manifests and the Claude marketplace entry together when publishing an update.

## Support and policies

- [Report a plugin issue](https://github.com/qawolf/agent-plugins/issues)
- [QA Wolf documentation](https://docs.qawolf.com)
- [Privacy policy](https://www.qawolf.com/legal/privacy-policy)
- [Terms](https://www.qawolf.com/legal/terms)

Do not post API keys, passwords, or customer test data in public issues.
