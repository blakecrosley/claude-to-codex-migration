# Source Research and Browser Tooling

Use this reference before porting Claude browser automation, web-research commands, source-verification MCP, or private browsing tools into Codex.

## Goal

Preserve source accuracy and rendered-behavior verification without publishing private tool names, local paths, credentials, browser workflows, or proprietary research process.

## Classification

Map each research surface to the smallest Codex primitive that proves the job:

| Source Need | Codex Shape | Default State |
| --- | --- | --- |
| Current public tool behavior | Official docs, primary sources, and cited web research | active through the relevant research/profile workflow |
| Public article citation verification | Citation checker plus public-writing review profile | pilot or enforced only for changed public Markdown |
| Local rendered behavior | Browser skill/plugin, Playwright, or direct runtime check | explicit-only or task-local |
| Private browser automation | Private CLI/profile/tool config | parked or explicit-only |
| Reusable third-party MCP | Private MCP config or sanitized `.mcp.example` | parked until scoped |
| Public plugin MCP | Plugin MCP manifest with no secrets and minimal tool exposure | publish only after real-task proof |

## Migration Rules

1. Do not treat a Claude MCP server or browser command as automatically plugin-worthy. First identify the verification job it performs.
2. Prefer official docs and primary sources for current public claims. Public content should cite those sources directly and label local experiments as author analysis.
3. Prefer a local browser skill or direct runtime check for rendered local behavior. Do not convert browser control into public plugin surface unless repeated users need that capability.
4. Keep private browser automation and private MCP names out of public articles, plugin manifests, examples, screenshots, and registries intended for sharing.
5. If a local tool's own Codex skill recommends CLI over MCP, use the CLI path and keep MCP parked until the MCP route is stable.
6. If MCP is needed, start private: no public manifest, no credentials, minimal `enabled_tools`/`disabled_tools`, and one explicit profile or task that proves the value.
7. Record evidence in the private monitor as sanitized behavior: source type, command category, pass/fail result, and what remains unverified. Avoid raw paths, raw tokens, exact browser scripts, and private provider names in public-facing artifacts.

## Official Docs MCP

An official documentation MCP can be useful for source-verification tasks, but it is still a local capability until Codex exposes the server in a restarted session and a real task proves better results than direct official web pages.

Keep official docs MCP setup local by default:

- Add it as a user MCP server only when it improves current-claim verification.
- Validate with `codex mcp list` and a config parse.
- Treat current-session MCP tool discovery as unverified until a restarted session exposes the tools.
- If the MCP tools are unavailable, fall back to official documentation pages and cite those pages directly.
- Do not add an MCP manifest to the public plugin unless repeated source-verification tasks prove that users need the bundled integration.

## Promotion Gates

Before promoting source-research tooling beyond parked or explicit-only:

- Codex config parses successfully.
- Any MCP config lists cleanly and exposes only the intended tools.
- One real source-verification task passes with citations or captured rendered behavior.
- Public copy uses primary-source citations for external/tool claims.
- Private paths, exact tool names, tokens, session IDs, and browser workflow details are absent from public artifacts.
- Failure behavior is documented: what to do if the browser/MCP path is unavailable.

## Public-Writing Boundary

For public migration articles, describe the pattern, not the private machinery:

- Safe: "we used a private source-verification lane to check current docs and rendered behavior."
- Safe: "local hook telemetry showed category counts only and did not log raw changed lines."
- Unsafe: exact private MCP names, raw local paths, prompt bodies, hook bodies, browser scripts, account identifiers, or unpublished writing workflow details.

The public article can say the migration uses a learning loop. It should not publish the harness internals that create the loop.
