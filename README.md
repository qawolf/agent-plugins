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

## Release automation

Automatic publishing starts after the backend release integration is deployed and its GitHub app has access to this repository.

The QA Wolf backend release pipeline manages `plugins/qawolf` and the QA Wolf entry in each marketplace. Plugin changes belong in the platform source, not in this repository's generated bundle.

After a successful backend release, the sync copies the approved plugin files from the released commit. It increments the public patch version when content changes and uses the same version in both manifests and the Claude marketplace. Unchanged releases do not create commits. The sync preserves this README and unrelated repository files.

Repository updates do not publish a new version in OpenAI's official directory. That directory requires a separate scan, review, and publication step.

## Support and policies

- [Report a plugin issue](https://github.com/qawolf/agent-plugins/issues)
- [QA Wolf documentation](https://docs.qawolf.com)
- [Privacy policy](https://www.qawolf.com/legal/privacy-policy)
- [Terms](https://www.qawolf.com/legal/terms)

Do not post API keys, passwords, or customer test data in public issues.
