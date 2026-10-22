# MCPShield

<div align="center">
  <img src="https://raw.githubusercontent.com/dntaskmehow/mcpshield/main/assets/mcpshield-mark.svg" alt="MCPShield" width="120" />
  <h1>MCPShield</h1>
  <p><strong>Model Context Protocol Security Gateway &amp; Least-Privilege Policy Enforcer for AI Agents</strong></p>

  <p>
    <a href="https://github.com/dntaskmehow/mcpshield"><img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" /></a>
    <a href="https://opensource.org/licenses/MIT"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-green.svg" /></a>
    <a href="https://github.com/dntaskmehow/mcpshield"><img alt="MCP Security" src="https://img.shields.io/badge/Focus-MCP%20Security-0f172a?logo=github&logoColor=white" /></a>
    <a href="https://github.com/dntaskmehow/mcpshield"><img alt="Language: Python" src="https://img.shields.io/badge/Language-Python-100%25-3776AB?logo=python&logoColor=white" /></a>
  </p>

  <p>
    <img alt="Stack" src="https://img.shields.io/badge/Stack-pydantic%20%7C%20rich-0f172a?logo=python&logoColor=white" />
  </p>
</div>

MCPShield is a lightweight security gateway for Model Context Protocol (MCP) tool calls. It inspects agent-to-tool requests against a policy file and blocks access when an agent attempts to invoke an unapproved tool or passes dangerous arguments.

The goal is simple: enforce least privilege before an AI agent can reach an external tool, script, or command surface.

## Why MCPShield exists

AI agents increasingly call tools and systems with broad or implicit trust. Without a guardrail, a request can easily drift into:

- unauthorized tool invocation,
- dangerous argument patterns such as shell escapes or path traversal,
- broad execution access that exceeds the agent's intended role.

MCPShield adds a narrow enforcement layer that checks each request against policy before it is approved.

## At a glance

- Enforces per-agent allowlists for MCP tools.
- Rejects calls that match blocked patterns in tool arguments.
- Uses a JSON policy file for simple policy management.
- Runs as a Python CLI with no extra runtime dependencies beyond the project itself.
- Produces structured JSON results for approval, denial, and reasons.

## Key capabilities

### Policy-based authorization

Each agent is assigned a policy entry with:

- `allowed_tools`: the list of tools the agent may invoke
- `blocked_patterns`: dangerous argument patterns to deny

If a tool call is not explicitly allowed, or if any argument contains a blocked pattern, access is denied.

### Argument inspection

The gateway inspects each argument value as a string and checks it against configured blocked patterns such as:

- `;`
- `rm -rf`
- `drop table`
- `../../`

This is intended as a lightweight yet immediately useful safety check for agent tool invocations.

### Security-first output

The CLI prints JSON results showing whether a call was authorized and why. This makes the tool suitable for automation, preflight checks, and secure agent tooling workflows.

## How it works

```text
AI Agent -> ToolCallRequest -> MCPShieldGateway -> policy evaluation -> allow / deny
                          |
                          +-> allowed_tools check
                          +-> blocked_patterns scan
                          +-> JSON authorization result
```

The project is intentionally small and focused: one CLI entry point, one gateway, and one request model.

## Installation

From a local clone of the repository:

```bash
python -m pip install -e .
```

This installs the `mcpshield` CLI entry point defined in `pyproject.toml`.

## Quick start

Create a policy file such as `policy.json`:

```json
{
  "research-agent": {
    "allowed_tools": ["search_docs", "read_file"],
    "blocked_patterns": [";", "rm -rf", "drop table", "../../"]
  },
  "ops-agent": {
    "allowed_tools": ["deploy_service"],
    "blocked_patterns": [";", "rm -rf", "../../"]
  }
}
```

Then invoke the CLI:

```bash
mcpshield --policy policy.json --agent research-agent --tool search_docs --args '{"query":"security policy", "limit":5}'
```

Example approved result:

```json
{
  "authorized": true,
  "reason": "Request inspected and approved by MCPShield."
}
```

Example denied result:

```json
{
  "authorized": false,
  "reason": "Security violation: Malicious pattern 'rm -rf' detected in argument 'command'."
}
```

## Usage

```bash
mcpshield --help
```

### Supported arguments

- `--policy`: path to the JSON policy file
- `--agent`: agent identifier to evaluate
- `--tool`: tool name being invoked
- `--args`: JSON-encoded argument payload for the request

## Example policy model

```json
{
  "agent-id": {
    "allowed_tools": ["tool_a", "tool_b"],
    "blocked_patterns": [";", "rm -rf", "drop table", "../../"]
  }
}
```

This simple structure keeps policy review readable while still enabling least-privilege enforcement.

## Technical details

MCPShield is implemented in Python 3.10+ and uses:

- `pydantic` for request validation
- `rich` for terminal presentation and reporting support
- a minimal JSON-based policy model for permission enforcement

The core logic is intentionally compact. The gateway reads a JSON policy, evaluates the requested tool against the current agent, and denies calls when the request violates the allowlist or blocked-pattern model.

## Security and responsible use

MCPShield is a defensive security tool intended for controlled environments and authorized AI system review. It should be used to reduce unsafe tool access and enforce guardrails within systems you operate or assess.

Do not deploy it as a substitute for broader application security controls, identity boundaries, or upstream validation of privileged system operations.

## Contributing

Contributions are welcome. The project is intentionally compact, so meaningful improvements typically fall into one of these areas:

- more advanced policy evaluation rules,
- richer structured outputs,
- additional guardrail patterns,
- stronger documentation and practical examples.

## License

This project declares MIT licensing in `pyproject.toml`.

## Project status

MCPShield is a focused security gateway for MCP-based agent access control. It is best understood as a practical enforcement layer for least-privilege AI tool access rather than a full enterprise control plane.

---

<div align="center">
  <p><em>Security by policy, not by assumption.</em></p>
</div>
