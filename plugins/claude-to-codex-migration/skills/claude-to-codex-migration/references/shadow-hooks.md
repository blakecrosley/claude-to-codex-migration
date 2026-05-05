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

## Codex Changed Public Markdown Citation Stop

For a Codex port of the citation checker, scope the Stop hook to changed public Markdown only. Use Git status from the current working directory, then filter to public content paths such as `content/blog/` and `content/guides/`. Do not scan the full repository on every Stop event.

Use `Stop` JSON with `decision = "block"` when changed public Markdown has missing or duplicate footnote definitions. That creates a continuation prompt, so the hook should also pass when `stop_hook_active` is true to avoid a repeated-block loop.

Keep unused definitions advisory while a known cleanup backlog exists. Missing and duplicate definitions are the first pilot failures because they affect reader-visible citations directly. Add a documented local bypass and log only file counts and failure counts.

When more than one `Stop` hook is active, validate combinations before promotion: one hook blocking while another passes, multiple hooks blocking the same first response, and the continuation response. Every `Stop` hook must pass when `stop_hook_active` is true; otherwise independent gates can create a repeated-block loop. If multiple gates can block the same response, keep reasons short and watch whether the continuation remains readable before promoting beyond pilot.

## Codex Post-Patch Quality Shadow

Do not assume Claude `PostToolUse:Edit|Write` maps directly to Codex. In local Codex runtime probes, file edits surfaced as `PostToolUse` with `tool_name` set to `apply_patch`, and the patch body was available at `tool_input.command`. Shell commands surfaced as `tool_name` `Bash`.

For a Codex port of post-edit quality checks, start with a non-blocking `PostToolUse` hook matched on `apply_patch`. Parse only changed patch lines first. This avoids turning old file debt into new hook noise.

Keep this class of hook in `shadow` or advisory mode until real tasks prove signal quality. For `PostToolUse`, plain stdout is ignored; return JSON with `hookSpecificOutput.hookEventName = "PostToolUse"` and `hookSpecificOutput.additionalContext` when findings should become model-visible context. Noisy findings will affect the agent's next step even when the hook does not block.

For signal/noise review, log category counts rather than raw changed lines. Before promotion, test at least one known-bad fixture and one known-noisy fixture. Scope broad text patterns such as hardcoded-secret and shortcut-language checks to code/config-like files; documentation and public-writing Markdown often contains examples that should not become hook noise.

Before wider activation, sanitize model-visible paths to cwd-relative or home-relative form and omit line numbers when the added text is ambiguous, such as duplicate exact lines in the final file. Advisory output should be useful without exposing local absolute paths. Keep Python ignore-pattern checks narrow: a bare `except:` or bare `except: pass` is high-confidence signal, but `except OSError: pass` and similar specific-exception handling needs project-specific evidence before it becomes hook noise.

## Codex Pre-Bash Safety Guard

Do not port a Claude pre-bash dispatcher wholesale. In local Codex runtime probes, shell commands surfaced as `PreToolUse` with `tool_name` set to `Bash` and the command string available at `tool_input.command`.

For a Codex port of destructive-command and credential-file checks, start with one narrow `PreToolUse` hook matched on `Bash`. Block only deterministic, high-confidence cases first: direct credential-file reads, full environment dumps, obvious destructive filesystem commands, destructive git commands, and destructive API/tool operations.

Shell init files are not automatically secret files, but they often become accidental credential carriers. If a direct-print command or credential-name search targets a shell init file that actually contains credential-shaped exports, block the read without echoing file contents, raw values, or absolute private paths in the reason.

For blocking, return JSON with `hookSpecificOutput.hookEventName = "PreToolUse"`, `hookSpecificOutput.permissionDecision = "deny"`, and `hookSpecificOutput.permissionDecisionReason`. Keep the reason actionable, but do not echo secrets or raw credential values.

Keep this class of hook in `pilot` until real task runs prove false positives are low. Add a documented local bypass for intentional escape, log only categories and decisions, and do not port any credential availability injection into public/plugin artifacts. Secrets should never be added to model-visible context.

## Codex SessionStart Context

Use `SessionStart` for compact context that should apply once per session: current date from the local clock, project basename, start source, and a reminder that current public claims need primary-source verification. Return JSON with `hookSpecificOutput.hookEventName = "SessionStart"` and `hookSpecificOutput.additionalContext`; plain stdout also works, but JSON keeps the intent explicit.

Do not use a session-start hook as a private prompt dump. Keep full paths, private tool names, exact hook internals, account identifiers, and unpublished workflow details out of model-visible context. Log only source/project/category-level telemetry.
