---
name: claude-to-codex-migration
description: Plan and execute public-safe Claude Code to Codex migrations by mapping CLAUDE.md, slash commands, hooks, skills, agents, MCP, profiles, and project rules into Codex AGENTS.md, config profiles, skills, hooks, MCP servers, verification checks, staged activation states, and a learning loop. Use when migrating a Claude Code setup to Codex, building a Codex harness, packaging the migration as a plugin, or auditing what should become AGENTS rules, profiles, skills, hooks, or MCP.
metadata:
  short-description: Migrate Claude Code harnesses to Codex
---

# Claude to Codex Migration

Use this skill to move a Claude Code harness into Codex without leaking private implementation details. The output should be a working Codex configuration, a private migration checklist, a staged rollout registry, and optionally a sanitized public write-up.

## Safety Boundary

Keep these private unless the user explicitly narrows the scope and confirms the destination is private:

- Private prompts, skill bodies, and unpublished philosophy documents.
- Exact hook internals, router logic, command bodies, and proprietary verification workflows.
- Sensitive local paths, raw inventories, private filenames, keys, tokens, and account identifiers.
- Client, employer, or brand-specific writing workflows that are not already public.

For public artifacts, describe the pattern and the acceptance criteria. Do not disclose the private machinery.

## Core Workflow

1. Inventory the Claude Code harness surfaces with local file discovery. Prefer `rg --files`, `rg`, `find`, and direct config reads. Separate public facts from private implementation details.
2. Classify each surface into a Codex primitive:
   - `AGENTS.md`: durable project policy, definitions of done, security rules, and quality bars.
   - `config.toml` profiles: repeatable execution posture, model reasoning effort, sandboxing, approvals, and search behavior.
   - Skills: reusable domain workflows that Codex should trigger by task description.
   - Hooks: deterministic lifecycle checks that should run without model discretion.
   - MCP/tooling: external systems, browsers, repositories, docs, search, and data sources.
   - Plugins: shareable packaging for skills, hooks, MCP, apps, and marketplace metadata.
3. Port the highest-value pieces first:
   - Global and project `AGENTS.md` rules that define the outcome standard.
   - One or two profiles for careful work and public-facing writing/review.
   - The most-used reusable workflow as a Codex skill.
   - Narrow verification hooks only after the manual process is stable.
4. For active local iteration, keep the migration workflow available as a user or repo skill. Treat a plugin as packaging until it is installed, enabled, restarted into a new session, and visible to Codex.
5. Stage each migrated piece before enabling it broadly. Use explicit-only skills, named profiles, omitted hook manifests, and omitted MCP manifests until tests prove the behavior.
6. Validate current Codex behavior against local CLI help and official OpenAI Codex docs before publishing technical claims.
7. Record a private migration monitor with completed work, remaining gaps, activation state, evidence, and public/private boundaries.
8. If writing publicly, publish sanitized aggregate findings and cite official docs for Codex behavior.

## Artifact Map

| Claude Code Surface | Codex Target | Migration Rule |
| --- | --- | --- |
| `CLAUDE.md` | `AGENTS.md` | Move durable operating policy and quality rules. |
| Slash command | Skill or small wrapper command | Use a skill for reusable reasoning workflow; use a command only as a convenience launcher. |
| Hook | Codex hook or script | Port only deterministic checks with clear pass/fail criteria. |
| Subagent | Skill, profile, or delegated workflow | Preserve the job-to-be-done, not the exact agent framing. |
| MCP config | Codex MCP config/plugin metadata | Keep external tool access explicit and documented. |
| Philosophy note | `AGENTS.md` principle or private reference | Convert doctrine into behavior gates; keep private source material private. |
| Blog/writing workflow | Private skill plus verification profile | Publish only the editorial standard, not proprietary process details. |

## Staged Rollout Loop

Treat the migration as a loop, not a one-time port:

1. Capture the candidate component in a private registry.
2. Package the smallest Codex equivalent without enabling it globally.
3. Test with one real task and record what happened.
4. Promote, revise, or retire the component.
5. Update the plugin instructions when the process changes.
6. Update the public post only with sanitized findings and verified Codex behavior.

Use these activation states:

| State | Meaning |
| --- | --- |
| `parked` | Captured but not exposed to Codex runtime. |
| `packaged` | Files exist but are not referenced by a plugin manifest or config. |
| `explicit-only` | Usable only when directly invoked or selected. |
| `pilot` | Enabled for one profile, repo, or narrow workflow. |
| `shadow` | Runs as a non-blocking check and records evidence. |
| `enforced` | Blocks or strongly governs normal work. |
| `retired` | Removed from active migration because it did not pay for its complexity. |

Read `references/staged-rollout.md` before adding private harness modules, dormant hooks, MCP config, or profile snippets.

## Skill vs Command

Default to a skill for the migration itself. A skill is the durable Codex unit for reusable task behavior, because it can carry instructions, references, scripts, and UI metadata.

While the workflow is still changing, install or mirror the active skill into `$HOME/.agents/skills` or repo `.agents/skills` and validate it there. A local plugin package can exist in parallel for sharing, but the package is not the runtime path until Codex installs it from a marketplace, loads it in a restarted session, and exposes its bundled skill.

Expect plugin-installed skills to appear under a plugin namespace such as `plugin-name:skill-name`. Keep examples clear about whether they are invoking the direct user/repo skill or the plugin-installed namespaced skill.

Use a command only when the user wants a short launcher such as "run the migration checklist" or "start the public-safe port." The command should call the skill or insert a prompt. It should not contain the canonical migration logic.

Use a plugin when the user wants to distribute the work on GitHub or expose it through a Codex marketplace. A plugin can bundle the skill now and later add hooks, MCP config, app entries, or scripts.

## Acceptance Criteria

Before calling a migration done:

- Codex config parses successfully.
- Intended profiles exist and are usable by name.
- `AGENTS.md` files state durable quality rules without exposing private material.
- New or ported skills validate with the skill validator.
- The active migration skill is present in a user/repo skill location or the plugin-installed copy is visible after restart; otherwise report runtime discovery as unverified.
- Hooks, if added, are deterministic and have a manual bypass or documented failure behavior.
- Public-facing content has citations for tool behavior and avoids raw private inventory.
- Final responses state what remains unverified when the work touches public content, harness behavior, or staged activation.
- The user can tell what changed, what remains, and what is safe to publish.

## Optional References

Read `references/public-packaging.md` when deciding whether a migration should be published as a standalone skill, plugin repo, marketplace entry, or wrapper command.

Read `references/staged-rollout.md` when deciding how to keep migrated harness parts inactive until they pass real task tests.

Read `references/doctrine-migration.md` when migrating philosophy, quality doctrine, taste rules, evidence rules, or other operating principles into Codex.

Read `references/shadow-hooks.md` before creating or enabling Codex hook candidates.

Read `references/final-verification-summary.md` before testing or promoting final-answer verification gates.

Read `references/source-research.md` before porting browser automation, web research, source-verification MCP, or private browsing tools.
