# Public Packaging

Use this reference when the user wants to share a Claude Code to Codex migration workflow publicly.

## Recommended Shape

Keep the active migration workflow as a user or repo skill while it is still changing. Package the same workflow as a Codex plugin containing one skill when the goal is sharing, installation, or future marketplace metadata.

A plugin folder on disk is not the same thing as an installed runtime plugin. Verify plugin installation by restarting Codex and confirming the plugin or bundled skill appears in the plugin/skill UI. Until then, the user/repo skill is the active runtime path and the plugin is the package.

When the plugin-installed skill loads, Codex may expose it with the plugin namespace, for example `claude-to-codex-migration:claude-to-codex-migration`, while the direct user skill remains `claude-to-codex-migration`.

Add executable scripts only when the operation is deterministic, inspectable, and safe to run against another user's configuration. Avoid scripts that read broad home-directory state, scrape private prompts, or publish raw inventories.

Keep the public plugin separate from the private harness. The public plugin can carry the method, staging model, and safe examples. A private plugin or private skill folder should carry real internal workflows, private prompts, exact hook logic, and sensitive local integration details.

## GitHub Layout

For a public repository that supports a simple marketplace command:

```text
claude-to-codex-migration/
├── .agents/
│   └── plugins/
│       └── marketplace.json
└── plugins/
    └── claude-to-codex-migration/
        ├── .codex-plugin/
        │   └── plugin.json
        └── skills/
            └── claude-to-codex-migration/
                ├── SKILL.md
                ├── agents/
                │   └── openai.yaml
                └── references/
                    └── public-packaging.md
```

This shape lets users add the marketplace with `codex plugin marketplace add owner/repo` after the repository is published. Codex resolves each marketplace `source.path` relative to the marketplace root, so keep the plugin under `./plugins/<plugin-name>`.

A bare plugin repository can still work when another marketplace points to it as a Git-backed plugin source, but it is not the cleanest first public artifact if the user-facing promise is one install command.

## Distribution Decision

- Skill only: best for a private team or a simple copy/clone install.
- Skill plus plugin package: best while iterating locally and preparing public distribution.
- Plugin only: best after install, restart, and discovery have been verified.
- Wrapper command: best for launching the skill with a canned prompt.
- Installer command: defer until the manual plugin has been tested by real users.

## Public Boundary

Public documentation may include artifact types, migration order, verification criteria, and sanitized examples. It should not include private prompts, exact hook internals, raw inventories, sensitive local paths, proprietary editorial processes, or unpublished philosophy material.
