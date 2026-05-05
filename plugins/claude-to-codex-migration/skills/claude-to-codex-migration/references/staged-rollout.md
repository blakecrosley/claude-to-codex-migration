# Staged Rollout

Use this reference when porting a real harness gradually instead of enabling every migrated component at once.

## Core Rule

Never make a private harness component globally active at the same time it is first ported. Port it, test it, then promote it.

## Activation Levers

Use the right lever for each Codex primitive:

| Primitive | Safe inactive state | Promotion path |
| --- | --- | --- |
| Skill | `agents/openai.yaml` with `allow_implicit_invocation: false`, or `[[skills.config]] enabled = false` in `~/.codex/config.toml` | explicit invocation, then implicit invocation |
| Profile | Named profile exists but is not the default | run with `codex -p <profile>` |
| Hook | Keep hook drafts outside `./hooks/hooks.json` and omit `hooks` from `plugin.json` | shadow hook, then enforcing hook |
| MCP | Keep config as `.mcp.example.json` or a private reference, not as manifested `.mcp.json` | add `mcpServers` only after the server is scoped and tested |
| Plugin | Marketplace entry uses `AVAILABLE`, not `INSTALLED_BY_DEFAULT`; active workflow still lives as a user/repo skill while iterating | manual install, restart, verify discovery, then default install if appropriate |
| AGENTS rule | Add narrow rule to the closest relevant scope | broaden only after observed behavior improves |

Codex also checks `./hooks/hooks.json` by default when it exists in a plugin. Do not place draft hook config at that path until the hook is ready to be loaded.

## Learning Loop

For each component:

1. Define the job it does in plain language.
2. Identify the Codex primitive that should own that job.
3. Choose an inactive or explicit-only state.
4. Run one real task that should benefit from it.
5. For hooks, profiles, routers, and other always-on surfaces, run a watch pass after real use. Summarize counts, categories, false positives, privacy exposure, and bypass behavior without copying raw private logs into public artifacts.
6. Record evidence: prompt, task type, expected behavior, actual behavior, failure mode, watch result, and next decision.
7. Promote only if it improves outcomes without adding confusing routing or false positives.
8. Feed the lesson back into the migration skill and private monitor.

## Promotion Gates

Promote from `parked` to `packaged` when the Codex target is obvious.

Promote from `packaged` to `explicit-only` when the files validate and do not expose private material beyond their intended scope.

Promote from `explicit-only` to `pilot` when a real task shows value. Pilot does not require implicit activation; a skill can remain explicit-only while being piloted for one repo or workflow.

Promote from `pilot` to `shadow` or `enforced` only when failures are understandable and the bypass path is clear.

Do not promote a hook from `pilot` or `shadow` on setup tests alone. Require at least one real-use watch pass that shows the hook is firing in the intended situations, passing ordinary work, logging only safe aggregate telemetry, and failing with a reason the user can act on.

Retire anything that needs too much explanation, duplicates a stronger Codex primitive, or makes routing less predictable.

## Public Article Feedback

The article should learn from the migration, but only at the pattern level:

- Good: "we staged hooks as non-blocking checks before enforcing them."
- Good: "we moved durable policy into AGENTS.md and kept task workflows as skills."
- Avoid: exact private prompt text, raw inventory rows, hook source, local script names, private tool names, or proprietary writing workflow details.
