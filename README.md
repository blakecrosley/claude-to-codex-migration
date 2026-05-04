# Claude to Codex Migration

Public-safe Codex plugin package for migrating a Claude Code setup into Codex primitives:

- `AGENTS.md` operating rules
- Codex profiles
- reusable skills
- deterministic shadow checks
- MCP/tooling decisions
- staged rollout records

The package intentionally contains process guidance, generic checks, and public examples. It does not contain private prompts, private writing workflows, raw inventories, exact internal hook logic, sensitive paths, or unpublished philosophy notes.

## Install

After publishing this folder as a GitHub repository, add it as a Codex plugin marketplace:

```bash
codex plugin marketplace add blakecrosley/claude-to-codex-migration
```

Then install or enable the plugin from the Codex plugin surface and start a fresh Codex session. Until plugin installation is verified in your runtime, use the skill directly from a user or repo skill folder:

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
python3 /path/to/quick_validate.py plugins/claude-to-codex-migration/skills/claude-to-codex-migration
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool plugins/claude-to-codex-migration/.codex-plugin/plugin.json
```

For the citation checker:

```bash
python3 plugins/claude-to-codex-migration/skills/claude-to-codex-migration/scripts/check_markdown_citations.py /path/to/article.md
```

Use `--allow-unused` while cleaning legacy content with stale citation definitions. Do not enforce unused-definition failures until cleanup debt is understood.

## License

MIT.
