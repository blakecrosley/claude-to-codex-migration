# Claude to Codex Migration

> Pre-release: this package is parked while the migration harness and article are being finished. Do not install it as an active Codex marketplace yet.

Public-safe Codex plugin package for migrating a Claude Code setup into Codex primitives:

- `AGENTS.md` operating rules
- Codex profiles
- reusable skills
- deterministic shadow checks
- MCP/tooling decisions
- staged rollout records

The package intentionally contains process guidance, generic checks, and public examples. It does not contain private prompts, private writing workflows, raw inventories, exact internal hook logic, sensitive paths, or unpublished philosophy notes.

## Install

After the package is marked ready, add this repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add blakecrosley/claude-to-codex-migration
```

Then install or enable the plugin from the Codex plugin surface and start a fresh Codex session. Marketplace add makes the plugin catalog available; runtime use still requires the plugin to be enabled and loaded. Until plugin installation is verified in your runtime, use the skill directly from a user or repo skill folder:

```text
$HOME/.agents/skills/claude-to-codex-migration/
```

Codex skills are the authoring format for reusable workflows. Plugins are the installable distribution unit for sharing those workflows.

Direct user/repo skill invocation uses:

```text
$claude-to-codex-migration
```

After plugin installation, Codex may expose the bundled skill with the plugin namespace:

```text
$claude-to-codex-migration:claude-to-codex-migration
```

## What This Includes

- A migration skill at `plugins/claude-to-codex-migration/skills/claude-to-codex-migration/`.
- A Codex plugin manifest at `plugins/claude-to-codex-migration/.codex-plugin/plugin.json`.
- A marketplace entry at `.agents/plugins/marketplace.json`.
- Public references for packaging, staged rollout, doctrine migration, shadow hooks, and final verification.
- A generic Markdown footnote citation checker for shadow testing.

## Recommended Use

1. Inventory the source Claude Code setup.
2. Classify each piece into Codex `AGENTS.md`, profiles, skills, hooks, MCP, or plugin packaging.
3. Move the highest-value rules first.
4. Keep active workflows as user or repo skills while they are changing.
5. Package stable workflows as plugins only after validation.
6. Keep hooks in shadow until they pass on real files and fail on known-bad examples.
7. Publish only sanitized patterns and verified tool behavior.

## Verification

From the repository root:

```bash
python3 scripts/validate_package.py
```

The package validator checks the marketplace JSON, plugin manifest, skill frontmatter, required references, citation-checker syntax, default installation policy, absence of active hooks/MCP manifests, and obvious private-path or secret-fixture leaks.

For the citation checker:

```bash
python3 plugins/claude-to-codex-migration/skills/claude-to-codex-migration/scripts/check_markdown_citations.py /path/to/article.md
```

Use `--allow-unused` while cleaning legacy content with stale citation definitions. Do not enforce unused-definition failures until cleanup debt is understood.

## License

MIT.
