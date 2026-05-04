# Shadow Hooks

Use this reference before turning a migrated Claude hook into an active Codex hook.

## Rule

Write the deterministic checker first. Run it manually against real files. Record whether it catches real failures without false positives. Only then decide whether to add a Codex hook manifest.

Do not create `hooks/hooks.json` while the hook candidate is still parked or shadow-only.

## Citation Definition Checker

The bundled citation checker validates Markdown footnote references:

```bash
python3 plugins/claude-to-codex-migration/skills/claude-to-codex-migration/scripts/check_markdown_citations.py \
  /path/to/content/blog/article.md
```

It fails when:

- A `[^id]` reference has no matching `[^id]:` definition.
- A definition has no matching reference.
- A definition appears more than once.

Use `--json` for hook-compatible output. Use `--allow-unused` only during cleanup migrations where existing stale definitions are expected and should not block the run.

For legacy content repositories, start hook pilots with missing and duplicate definitions as the hard failures. Treat unused definitions as cleanup signal until the existing backlog is fixed. The checker's `--allow-unused` flag keeps unused-definition evidence in the output while allowing the command to pass.

When a broad scan finds existing unused definitions, create a cleanup backlog before changing enforcement. Record the affected file, definition id, definition line, and next action. Do not promote unused-definition failures to an enforcing hook until that backlog is empty or deliberately scoped out.

## Promotion Gate

Keep the checker in `shadow` until it passes on real public articles, fails on known-bad fixtures, and has been run across a representative content set. Promote toward an enforcing `Stop` hook only after false positives are low, cleanup debt is understood, and the bypass path is clear.

Before any promotion, run its local tests:

```bash
python3 -m unittest discover -s tests
```
