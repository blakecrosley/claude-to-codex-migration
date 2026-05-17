#!/usr/bin/env python3
"""Validate the public Claude to Codex migration package shape."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "claude-to-codex-migration"
SKILL = PLUGIN / "skills" / "claude-to-codex-migration"
REQUIRED_REFERENCES = {
    "doctrine-migration.md",
    "final-verification-summary.md",
    "public-packaging.md",
    "shadow-hooks.md",
    "source-research.md",
    "staged-rollout.md",
}
PRIVATE_PATTERNS = (
    "/" + "Users" + "/",
    "Yu" + "rei",
    "yu" + "rei",
    "HEAR" + "TED",
    "SESSION_CONTEXT_TEST_" + "SENTINEL",
    "TOKEN=" + "fixture",
    "API_" + "KEY=",
    ".codex/" + "hook-" + "logs",
    "mcp_" + "server",
)
PRODUCTION_GATE_PHRASES = {
    SKILL / "SKILL.md": (
        "verify the deployed user path",
        "sitemap inclusion",
        "llms-full.txt",
        "production or intended user path",
    ),
    SKILL / "references" / "staged-rollout.md": (
        "production/user-path check",
        "cache-busting URL",
        "stale CDN/cache response",
        "canonical production URL",
    ),
    ROOT / "README.md": (
        "production/user path",
        "canonical URL",
        "AI-discovery surfaces",
    ),
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def load_json(path: Path, failures: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON ({type(exc).__name__})", failures)
        return {}


def parse_skill_frontmatter(path: Path, failures: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)}: missing frontmatter fence", failures)
        return {}
    try:
        raw = text.split("---\n", 2)[1]
    except IndexError:
        fail(f"{path.relative_to(ROOT)}: malformed frontmatter", failures)
        return {}

    frontmatter: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter


def check_required_files(failures: list[str]) -> None:
    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / ".gitignore",
        ROOT / ".agents" / "plugins" / "marketplace.json",
        PLUGIN / ".codex-plugin" / "plugin.json",
        SKILL / "SKILL.md",
        SKILL / "agents" / "openai.yaml",
        SKILL / "scripts" / "check_markdown_citations.py",
    ]
    for path in required:
        if not path.exists():
            fail(f"missing required file: {path.relative_to(ROOT)}", failures)

    refs = {path.name for path in (SKILL / "references").glob("*.md")}
    missing_refs = sorted(REQUIRED_REFERENCES - refs)
    if missing_refs:
        fail(f"missing references: {', '.join(missing_refs)}", failures)


def check_marketplace(failures: list[str]) -> None:
    marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json", failures)
    plugins = marketplace.get("plugins") if isinstance(marketplace.get("plugins"), list) else []
    entry = next((item for item in plugins if item.get("name") == "claude-to-codex-migration"), None)
    if not entry:
        fail("marketplace missing claude-to-codex-migration entry", failures)
        return
    source = entry.get("source")
    if isinstance(source, str):
        source_path = source
    elif isinstance(source, dict):
        source_path = source.get("path")
        if "source" in source:
            fail("local marketplace source must not include legacy source.source wrapper", failures)
    else:
        source_path = None
    if source_path != "./plugins/claude-to-codex-migration":
        fail("marketplace plugin source path must be ./plugins/claude-to-codex-migration", failures)
    if entry.get("policy", {}).get("installation") != "AVAILABLE":
        fail("marketplace installation policy must remain AVAILABLE before launch", failures)


def check_plugin_manifest(failures: list[str]) -> None:
    manifest = load_json(PLUGIN / ".codex-plugin" / "plugin.json", failures)
    if manifest.get("name") != "claude-to-codex-migration":
        fail("plugin manifest name mismatch", failures)
    if manifest.get("skills") != "./skills/":
        fail("plugin manifest skills path must be ./skills/", failures)
    for forbidden in ("hooks", "mcpServers", "apps"):
        if forbidden in manifest:
            fail(f"plugin manifest must not include {forbidden} before launch", failures)


def check_skill(failures: list[str]) -> None:
    frontmatter = parse_skill_frontmatter(SKILL / "SKILL.md", failures)
    if frontmatter.get("name") != "claude-to-codex-migration":
        fail("skill frontmatter name mismatch", failures)
    if not frontmatter.get("description"):
        fail("skill frontmatter missing description", failures)

    agent_yaml = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "allow_implicit_invocation:" not in agent_yaml:
        fail("openai.yaml missing allow_implicit_invocation policy", failures)

    citation_checker = SKILL / "scripts" / "check_markdown_citations.py"
    try:
        compile(citation_checker.read_text(encoding="utf-8"), str(citation_checker), "exec")
    except SyntaxError as exc:
        fail(f"citation checker does not compile: {exc.msg}", failures)


def check_production_publication_gate(failures: list[str]) -> None:
    for path, phrases in PRODUCTION_GATE_PHRASES.items():
        if not path.exists():
            fail(f"production publication gate source missing: {path.relative_to(ROOT)}", failures)
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(
                    f"{path.relative_to(ROOT)} missing production publication gate phrase: {phrase}",
                    failures,
                )


def check_unwanted_files(failures: list[str]) -> None:
    unwanted_names = {"__pycache__", ".DS_Store", ".env", ".mcp.json", "hooks.json"}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name in unwanted_names or path.suffix == ".pyc":
            fail(f"unwanted generated or active-runtime file: {path.relative_to(ROOT)}", failures)


def check_private_leaks(failures: list[str]) -> None:
    text_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in {"", ".md", ".json", ".yaml", ".yml", ".py", ".txt"}
    ]
    for path in text_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PRIVATE_PATTERNS:
            if pattern in text:
                fail(f"private pattern {pattern!r} found in {path.relative_to(ROOT)}", failures)

    marketplace = (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    if re.search(r"INSTALLED_BY_DEFAULT|ENABLED_BY_DEFAULT", marketplace):
        fail("marketplace must not install or enable the plugin by default", failures)


def main() -> int:
    failures: list[str] = []
    check_required_files(failures)
    check_marketplace(failures)
    check_plugin_manifest(failures)
    check_skill(failures)
    check_production_publication_gate(failures)
    check_unwanted_files(failures)
    check_private_leaks(failures)

    if failures:
        print("FAIL package validation")
        for item in failures:
            print(f"- {item}")
        return 1

    print("PASS package validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
