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
| Plugin | Marketplace entry uses `AVAILABLE`, not `INSTALLED_BY_DEFAULT`; active workflow still lives as a user/repo skill while iterating | manual install, verify app-server plugin state, verify fresh-session skill discovery, then default install if appropriate |
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

For public articles or guides, add a production/user-path check before calling the loop done. Verify the canonical URL, expected rendered metadata, structured data, sitemap inclusion, and `llms-full.txt` or equivalent AI-discovery surface. If the app serves the new page only behind a cache-busting URL, treat the canonical path as failed until the stale CDN/cache response is purged through the existing deployment path.

For guide-maintenance skills, the real-use pass needs a stricter record than "the Markdown changed." Capture primary-source evidence, release feeds, model cards or benchmark tables when cited, local runtime help when the tool has a CLI, private/public guide sync, derivative surfaces such as cheatsheets, templates, rendered FAQ/JSON-LD, citation integrity, rendered route checks, AI-discovery regeneration, served discovery-route checks, historical or metadata-derived route alias checks, and skipped gates. Translation, commit, deploy, and live production verification stay unverified unless they actually run.

Treat exact product numbers as high-risk claims. Event counts, skill context budgets, hook type counts, CLI versions, activation semantics, feature-compatibility matrices, benchmark/model-card numbers, rendered structured-data copy, and concurrency limits should be rechecked against current primary docs or local runtime behavior before being carried forward. If the current docs no longer support a fixed cap, score, or compatibility claim, remove it or phrase the guidance around the supported workflow instead.

For secret/log hygiene gates, the real-use pass needs to prove surface separation, not just that an env var exists. Record which classes were checked (executable source, public/private docs, generated caches, session transcripts, shell snapshots, logs, and intentional secret stores), which intentional stores were excluded from "leak" findings, what helper credentials were converted to environment-required config, what history was redacted, what rotation remains separate from cleanup, and what prevention hook is still only manual, shadow, or enforced. Do not copy token values, exact paths, detector regexes, private log excerpts, or proprietary workflow details into public artifacts.

For blog-intelligence skills, the real-use pass needs to prove judgment, not volume. Record the source map, ranking, dedupe decisions, source quality, public/private boundary, editorial decision, and next operational route. A good scan can refuse a new article and instead route to guide maintenance, source verification, monitoring, or another harness loop.

For blog company-onboarding skills, the real-use pass needs to prove intake discipline, not file volume. Record the company target, output path, required intake coverage, generated file set, config-file existence checks, YAML/frontmatter validation, and no-secret/private-prompt scan. If the target, output path, or intake evidence is missing, stop without writing files and record the missing fields.

For source-intelligence skills, the real-use pass needs to prove bounded memory writes, not raw harvesting. Run a constrained dry-run first, verify each selected source actually fetched items, compare candidate volume against the user's tolerance, and only then allow a non-dry run. Record actual files written, dedupe behavior, source gaps, and whether the next route is monitoring, guide maintenance, blog intelligence, or no-op.

For discovery-seeding skills, the real-use pass needs to prove prompt quality and liveness, not indexing. Verify selected URLs before including them, reject dead URLs, generate one copy-pasteable prompt per intended platform, persist the platform/theme/URL-set rotation ledger, and state that crawl, index, rank, and AI Overview outcomes remain unobserved unless separately measured.

For blog i18n audit skills, the real-use pass needs to prove coverage judgment, not just route availability. First identify whether translations are local files, D1/database-backed, or hybrid. Then record the actual scripts found, credential gates, skipped D1 checks, local extraction results, locale-set drift, supported locales omitted from queue or smoke defaults, live route smoke if run, and any stale or optional script/content-path assumptions. If a live-smoke script lacks locale selection, add the smallest read-only selector before claiming omitted-locale route health. If a detector has stale content paths, harden it in no-write mode and test current-path, legacy-fallback, tracked-item, and duplicate-slug behavior before any translation execution. A green locale route smoke is not proof of complete translations.

For blog translation skills, the real-use pass needs to prove write gates before write execution. Record storage shape, explicit slug/locale or trusted queue source, credential state without values, detector/queue trust decision, dry-run/preview result when available, files changed, validation results, and the no-write reason when execution is blocked. Missing D1 credentials, missing explicit target, or a detector result that points at the whole back catalog should stop the run.

For AIO/SEO audit skills, the real-use pass needs to prove the audit can separate site defects from audit-tool limits. Run local inventory checks and live endpoint checks separately, then smoke a representative rendered page for canonical, meta description, parseable JSON-LD, expected schema types, and private-path leaks. If local and live results disagree, inspect dynamic routes, generated discovery files, and crawler bot-list freshness before reporting a fix.

For cross-agent collaboration skills, the real-use pass needs to prove orchestration, not deference. Record false findings Codex rejected, accepted findings Codex fixed, the static re-review output, runtime checks, and remaining safety boundaries. Collaboration wrappers should fail closed when anchors are missing, unreadable, dangling, outside the repo-visible scope, output is empty, or a timeout occurs.

For plugin install pilots, record the exact activation boundary separately from public release. Package validation, marketplace add, app-server `plugin/read`/`plugin/install`, post-install `plugin/list`, `skills/list`, fresh `codex exec` visibility, duplicate-marketplace cleanup, and release-gate blockers should all be captured before promotion. A local install pilot can be valid while the public release remains blocked.

The clean boundary after a successful local install pilot is: `install-pilot`, public release blocked, remote or GitHub marketplace install unverified. Keep the README pre-release marker, do not create final release evidence, and do not weaken the release gate until a clean remote install path passes.

## Promotion Gates

Promote from `parked` to `packaged` when the Codex target is obvious.

Promote from `packaged` to `explicit-only` when the files validate and do not expose private material beyond their intended scope.

Promote from `explicit-only` to `pilot` when a real task shows value. Pilot does not require implicit activation; a skill can remain explicit-only while being piloted for one repo or workflow.

Promote a plugin package to `install-pilot` only after the installed plugin is enabled, the bundled skill is visible under its installed namespace in a fresh session, and duplicate local/public marketplace entries have been cleaned up or explicitly documented.

Promote from `pilot` to `shadow` or `enforced` only when failures are understandable and the bypass path is clear.

Do not promote a hook from `pilot` or `shadow` on setup tests alone. Require at least one real-use watch pass that shows the hook is firing in the intended situations, passing ordinary work, logging only safe aggregate telemetry, and failing with a reason the user can act on.

Retire anything that needs too much explanation, duplicates a stronger Codex primitive, or makes routing less predictable.

## Public Article Feedback

The article should learn from the migration, but only at the pattern level:

- Good: "we staged hooks as non-blocking checks before enforcing them."
- Good: "we moved durable policy into AGENTS.md and kept task workflows as skills."
- Good: "we verified the canonical production URL and discovery surfaces before calling the article live."
- Good: "we proved guide-maintenance ports on real updates and reported translation/deploy gaps separately."
- Good: "we corrected stale event-count, skill-budget, and concurrency-limit claims instead of preserving source-harness numbers."
- Good: "we checked both generated discovery files and the served crawler route, then fixed a route mismatch instead of treating the static file as proof."
- Good: "we caught frontmatter guide slugs leaking into AI-discovery files and added canonical alias redirects for exposed guide URLs."
- Good: "we used an intelligence scan to route source drift into a guide-maintenance pass instead of drafting a duplicative article."
- Good: "we stopped a company-blog onboarding before file generation because the target company and output path were not explicit, then aligned the config file contract with the active blog writer core."
- Good: "we dry-ran a write-heavy source scanner, narrowed the scan, then allowed only a small private-memory write while recording source-reachability gaps."
- Good: "we generated discovery-seeding prompts only after verifying URLs, recording rotation state, and refusing to claim indexing outcomes."
- Good: "we found that the i18n audit was D1-backed, separated route smoke from coverage proof, and recorded stale optional script/path assumptions plus omitted supported locales instead of claiming an empty queue or green default smoke was complete."
- Good: "we refused blog translation execution because D1 credentials and explicit slug/locale were missing and the detector pointed at the full back catalog."
- Good: "we split AIO audits into local inventory, live endpoint checks, and rendered-page schema checks, then treated local/live disagreement as an audit-tool finding until root-caused."
- Good: "we treated a second-agent review as an input, then used local evidence, fail-closed anchors, static re-review, and runtime checks before accepting the result."
- Avoid: exact private prompt text, raw inventory rows, hook source, local script names, private tool names, or proprietary writing workflow details.
