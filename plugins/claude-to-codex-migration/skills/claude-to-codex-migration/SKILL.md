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
   - Private product/taste rituals and guide-maintenance workflows when they are core to the user's production loop.
   - Guide-maintenance skills should preserve the update pipeline while replacing credential-spelling command bodies with secret-managed environment handling.
   - Secret/log hygiene should be treated as its own migration gate. Separate intentional secret stores from executable source, public/private docs, generated caches, session transcripts, shell snapshots, and logs; convert helper credentials to environment-required config; redact model-visible history where high-confidence secrets appear; track rotation separately from source cleanup; publish only generic criteria and never token values, exact paths, detector internals, or private workflow machinery.
   - Guide-maintenance ports should be proven on at least one real update or no-change pass that checks primary sources, release feeds, model cards or benchmark tables when cited, local runtime help where available, private/public guide sync, derivative cheatsheets or templates, rendered structured-data templates, rendered routes, citation integrity, SEO/AIO discovery files, and explicit translation/deploy gaps.
   - Guide-maintenance ports that touch translated guide surfaces should prove the provider-selection path, default to the Codex-owned path when Codex is orchestrating, record translation-store credential state without values, run a differential dry-run or preview when available, and refuse "translated" or "release-ready" claims unless translation writes and locale verification actually ran.
   - Guide-maintenance ports should re-verify exact product counts, budgets, version claims, activation semantics, feature-compatibility matrices, benchmark/model-card numbers, rendered FAQ/JSON-LD copy, and feature parity against current primary sources. Do not preserve fixed event counts, context budgets, benchmark scores, concurrency caps, credit budgets, third-party-only feature minimums, undocumented API/private-beta assertions, or legal/indemnification claims from the source harness unless current primary docs or runtime evidence still supports them.
   - Guide-maintenance ports should verify generated discovery files, served crawler routes, and historical or metadata-derived route aliases separately. A correct static `llms-full.txt` is not proof if the application route bypasses it, and a frontmatter slug is not proof that the URL is served.
   - Blog intelligence workflows should preserve source verification, triage, deduplication, and coverage tracking without publishing proprietary scoring or editorial strategy.
   - Real intelligence scans should be allowed to refuse a new article and instead route the next operation to guide maintenance, source verification, monitoring, or another harness loop when that better serves readers.
   - Site-content workflows should preserve content invariants such as i18n, schema, AI-discovery surfaces, and deployment verification without embedding secrets or private publishing internals.
   - For blakecrosley.com publication flows, preserve the distinction between local proof, deployment proof, CDN freshness, and live user-visible proof. Railway status/deployment/log evidence, Cloudflare purge status for changed URLs and discovery files, and live changed-marker checks are separate gates; route `200` or local render success is not enough.
   - Blog operations should include the full production loop when the source harness depends on it: company onboarding, article writing standards, SEO/AIO checks, translation audit/translation, intelligence scanning, and post-publication discovery verification. Keep brand-specific prompts and scoring internals private.
   - Blog company-onboarding ports should fail closed when the company target, output path, or required intake evidence is missing. Align generated config filenames with the active blog-writer core and existing company-writer pattern, not stale Claude defaults.
   - Blog i18n audit ports should prove the project's actual translation storage, script shape, and supported-locale shape before running coverage claims. Record credential gates, local-only fallbacks, locale-set drift, stale or optional script names, omitted supported locales, and whether live route health is being separated from translation completeness.
   - Blog translation ports should prove credential and target gates before write execution. Missing D1 credentials, missing explicit slug/locale, or a full-back-catalog detector result should stop translation rather than enqueue or write.
   - Blog translation ports should support Codex and Claude providers, with `auto` resolving to Codex inside Codex-owned sessions and Claude outside them. They should treat title, description, and body as the source fingerprint; preserve link destinations while translating visible link text; merge checkpoints rather than replacing unrelated slugs; and run the local quality gate before D1 upload or checkpoint completion. A cache write, route `200`, or provider review pass is not enough by itself.
   - AIO/SEO audit ports should prove local inventory checks, live endpoint availability, representative rendered-page metadata/schema, and private-leak checks. When local audit output disagrees with live user-visible behavior, root-cause dynamic routing or stale crawler-vocabulary assumptions before filing a site defect.
   - Operational memory and source-intelligence rituals should be ported when they affect future work quality. Prefer explicit-only private skills for daily logs, signal scanners, and crawl/discovery seeding until real use proves they should be more automatic.
   - Source-intelligence ports should prove source reachability, dedupe behavior, write volume, and routing judgment on a constrained dry run before writing to private memory. A broad write batch is not a success signal.
   - Discovery-seeding ports should prove prompt generation, URL liveness, rotation state, and outcome humility. Generating prompts is not evidence of crawl, indexing, ranking, or AI Overview inclusion.
   - Cross-agent collaboration should be explicit, scoped, output-captured, fail-closed on missing, unreadable, dangling, or outside-repo anchors, timeouts, or empty output, and Codex-reviewed before any Claude output is accepted. A useful loop rejects false second-agent findings with local evidence, accepts only grounded findings, fixes the smallest real defect, reruns static re-review, and then runs Codex-owned verification.
   - Narrow verification hooks only after the manual process is stable.
4. For active local iteration, keep the migration workflow available as a user or repo skill. Treat a plugin as packaging until it is installed, enabled, restarted into a new session, and visible to Codex.
5. Stage each migrated piece before enabling it broadly. Use explicit-only skills, named profiles, omitted hook manifests, and omitted MCP manifests until tests prove the behavior.
6. Validate current Codex behavior against local CLI help and official OpenAI Codex docs before publishing technical claims.
7. Record a private migration monitor with completed work, remaining gaps, activation state, evidence, and public/private boundaries.
8. If writing publicly, publish sanitized aggregate findings and cite official docs for Codex behavior.
9. If the migration produces a public article, verify the deployed user path before calling it live: canonical URL, rendered metadata, structured data, sitemap inclusion, and `llms-full.txt` or the project's equivalent AI-discovery surface. If a CDN or cache preserves a stale response, record the sanitized failure mode and use the existing secret-managed purge/deploy path.

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
| Intelligence scanner | Explicit-only private Codex skill | Preserve source-quality rules, finding tiers, coverage tracking, and the ability to route findings away from article generation; publish only the generic methodology. |
| Site-content workflow | Explicit-only private Codex skill | Preserve i18n, schema, SEO/AIO, translation, and user-path checks; do not publish secrets or internal publishing mechanics. |
| Translation or i18n audit workflow | Explicit-only private Codex skill | Preserve queue, stale-content, validation, SEO, and locale-review checks; do not expose translation credentials or private cache internals. |
| AIO/SEO audit workflow | Explicit-only private Codex skill | Preserve llms.txt, schema, robots, sitemap, metadata, and user-path checks; publish only generic criteria and evidence requirements. |
| Operational memory log | Explicit-only private Codex skill | Preserve the session-capture job and searchable output shape; keep vault paths and sensitive operational details private. |
| Discovery seeding workflow | Explicit-only private Codex skill | Preserve the generation and rotation rules; do not claim crawl/indexing outcomes without observed evidence. |
| Cross-agent collab command | Explicit-only private Codex skill plus wrapper script | Let Codex ask Claude for plans, reviews, verification, or scoped implementation; isolate writes and verify locally before accepting. |
| Product/taste ritual | Explicit-only private Codex skill | Preserve the review job and quality gates; do not publish persona packs, prompt bodies, or arbitration internals. |
| Guide-maintenance command | Codex skill plus verification gates | Preserve the scan, compare, update, review, publish, sync, and report loop; publish only verified tool behavior; do not port hardcoded credential values. |
| Secret/log hygiene ritual | Manual gate, explicit-only skill, or narrow hook | Preserve the separation between source/docs/generated-cache/session/log scans and intentional secret stores; redact history and convert helpers to env-required config; never publish token values, exact paths, detector internals, or private workflow machinery. |

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
| `install-pilot` | Installed and enabled only for a narrow package-install proof, with public release still blocked. |
| `enforced` | Blocks or strongly governs normal work. |
| `retired` | Removed from active migration because it did not pay for its complexity. |

Read `references/staged-rollout.md` before adding private harness modules, dormant hooks, MCP config, or profile snippets.

## Skill vs Command

Default to a skill for the migration itself. A skill is the durable Codex unit for reusable task behavior, because it can carry instructions, references, scripts, and UI metadata.

Treat `$skill-name` as the canonical explicit invocation path. Codex skills are not Claude slash commands: `/skills` opens the skill selector and `$` mentions a skill, while CLI slash commands are a separate interactive control surface. A bare `/name` should be documented only as a convenience phrase, a selector action, or a small wrapper that prompts `Use $name ...`; it is not the proof of skill activation by itself.

When porting Claude slash commands, preserve the job-to-be-done, not the slash syntax. If the old command was a reusable reasoning workflow, port it as a skill and test `$skill-name`. If the user still needs the old `/name` muscle memory, add the thinnest launcher possible and keep the canonical workflow in the skill.

While the workflow is still changing, install or mirror the active skill into `$HOME/.agents/skills` or repo `.agents/skills` and validate it there. A local plugin package can exist in parallel for sharing, but the package is not the runtime path until Codex installs it from a marketplace, loads it in a restarted session, and exposes its bundled skill.

Expect plugin-installed skills to appear under a plugin namespace such as `plugin-name:skill-name`. Keep examples clear about whether they are invoking the direct user/repo skill or the plugin-installed namespaced skill.

For install pilots, distinguish the marketplace root from the marketplace file. `codex plugin marketplace add` takes the marketplace root or repo, while app-server plugin install/read calls use the marketplace JSON file path. After install, verify `plugin/list`, `skills/list`, and a fresh `codex exec` session. If a repo-local marketplace and public package marketplace both expose the same plugin, leave only the intended pilot installed and record the duplicate cleanup.

Use a command only when the user wants a short launcher such as "run the migration checklist" or "start the public-safe port." The command should call the skill or insert a prompt. It should not contain the canonical migration logic.

Use a plugin when the user wants to distribute the work on GitHub or expose it through a Codex marketplace. A plugin can bundle the skill now and later add hooks, MCP config, app entries, or scripts.

## Acceptance Criteria

Before calling a migration done:

- Codex config parses successfully.
- Intended profiles exist and are usable by name.
- `AGENTS.md` files state durable quality rules without exposing private material.
- New or ported skills validate with the skill validator.
- New active skills are loadable in a fresh Codex session through their intended trigger. For explicit-only skills, test `$skill-name` invocation; a generic metadata-visibility question or a bare `/name` prompt is not enough. If `/name` compatibility is promised, test the selector, wrapper, or routing path that makes it work. If runtime discovery differs by location, mirror or symlink the skill into a native Codex skill path or record the gap.
- The active migration skill is present in a user/repo skill location or the plugin-installed copy is visible after restart; otherwise report runtime discovery as unverified.
- Hooks, if added, are deterministic and have a manual bypass or documented failure behavior.
- Public-facing content has citations for tool behavior and avoids raw private inventory.
- Public-facing content is verified on the production or intended user path when publication is part of the work; local rendering alone is not enough to claim the live page works.
- Publication proofs distinguish local checks, Railway deploy state when available, Cloudflare purge/freshness state, and live changed-marker evidence. A green deploy plus stale public content is an incomplete release, not a success with a footnote.
- Guide-maintenance migrations record source evidence, changed public surfaces, benchmark/model-card or release-feed corrections when applicable, derivative template or structured-data changes, local route/render checks, discovery-file impact, served discovery-route checks, alias/redirect checks, and any skipped translation/deploy/live-production gates.
- Guide-maintenance migrations also record the selected translation provider, differential batch or section counts, credential state without values, whether translation writes/uploads occurred, locale verification results, and the no-write reason when execution is blocked.
- Secret/log hygiene migrations record scanned surface classes, intentional secret-store exclusions, helper-credential fixes, redaction state, rotation state, prevention-hook status, and remaining forensic-history gaps without values, exact paths, detector internals, or private workflow machinery.
- Blog-intelligence migrations record source map, ranking, dedupe decisions, source quality, public/private boundary, editorial decision, and the next operational route; do not treat every scan as an article prompt.
- Source-intelligence migrations record the dry-run gate, source-reachability gaps, candidate volume, actual files written when writing is allowed, and the next route. Do not claim a configured source worked unless the run fetched from it.
- Discovery-seeding migrations record generated prompts, verified URL statuses, rejected URLs, platform/theme rotation, a persisted ledger entry, and the explicit boundary that no crawl or indexing outcome was observed.
- Blog-operations migrations record which parts of the production loop are active: onboarding, writing, evaluation, SEO/AIO, i18n audit, translation, intelligence scanning, source seeding, and publication verification.
- Blog company-onboarding migrations record the intake fields collected, target/output path, generated config file set, config-file existence checks, YAML/frontmatter validation, no-secret/private-prompt scan, and no-write reason when onboarding stops before file generation.
- Blog i18n audit migrations record whether translations are file-backed or database-backed, the actual scripts found, credential-gated commands that were skipped, local source-key scan results, live locale-route smoke results when run, locale-set drift including omitted supported locales, stale or optional script/path assumptions, and the smallest safe next translation action.
- Blog translation migrations record storage shape, explicit slug/locale or trusted queue source, credential state without values, detector/queue trust decision, dry-run/preview result when available, files changed, validation results, and no-write reason when execution is blocked.
- Blog translation migrations also record the selected provider and auto-resolution behavior, whether the checkpoint includes title/description/body, whether focused runs preserve unrelated checkpoint entries, whether local gate pass blocks D1/checkpoint writes, whether visible markdown link text is localized while destinations remain stable, and whether any provider quota/auth/tool blocker prevented completion.
- AIO/SEO audit migrations record local audit score, live endpoint score, representative page canonical/meta/JSON-LD checks, private-leak check, root cause for local-vs-live disagreements, and any crawler bot-list assumptions that still need primary-source verification.
- Operational-memory migrations record where the log writes, whether it appends or creates, what evidence was captured, and what remains intentionally private.
- Cross-agent collaboration migrations record the accepted finding, any rejected second-agent findings, the fix path, static re-review output, local runtime checks, and remaining safety boundaries, including anchor readability and repo-locality checks; do not treat a second-agent approval as proof.
- Final responses state what remains unverified when the work touches public content, harness behavior, or staged activation.
- The user can tell what changed, what remains, and what is safe to publish.

## Optional References

Read `references/public-packaging.md` when deciding whether a migration should be published as a standalone skill, plugin repo, marketplace entry, or wrapper command.

Read `references/staged-rollout.md` when deciding how to keep migrated harness parts inactive until they pass real task tests.

Read `references/doctrine-migration.md` when migrating philosophy, quality doctrine, taste rules, evidence rules, or other operating principles into Codex.

Read `references/shadow-hooks.md` before creating or enabling Codex hook candidates.

Read `references/final-verification-summary.md` before testing or promoting final-answer verification gates.

Read `references/source-research.md` before porting browser automation, web research, source-verification MCP, or private browsing tools.
