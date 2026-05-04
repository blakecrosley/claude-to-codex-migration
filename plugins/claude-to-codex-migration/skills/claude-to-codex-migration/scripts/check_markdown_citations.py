#!/usr/bin/env python3
"""Check Markdown footnote references against definitions.

This is intended as a shadow hook candidate: run it manually first, record
signal/noise, and only wire it into hooks after it proves useful.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]\s]+)\]:")
FOOTNOTE_REF_RE = re.compile(r"\[\^([^\]\s]+)\]")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def iter_markdown_lines(path: Path) -> Iterable[tuple[int, str]]:
    in_fence = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield lineno, line


def strip_inline_code_spans(line: str) -> str:
    """Remove inline code spans so regex fragments are not parsed as footnotes."""
    stripped: list[str] = []
    index = 0

    while index < len(line):
        if line[index] != "`":
            stripped.append(line[index])
            index += 1
            continue

        tick_start = index
        while index < len(line) and line[index] == "`":
            index += 1
        tick_run = line[tick_start:index]
        closing = line.find(tick_run, index)

        if closing == -1:
            stripped.append(tick_run)
            continue

        index = closing + len(tick_run)

    return "".join(stripped)


def analyze_file(path: Path, allow_unused: bool) -> dict:
    refs: dict[str, list[int]] = {}
    defs: dict[str, list[int]] = {}

    for lineno, line in iter_markdown_lines(path):
        definition = FOOTNOTE_DEF_RE.match(line)
        if definition:
            defs.setdefault(definition.group(1), []).append(lineno)
            continue

        for ref in FOOTNOTE_REF_RE.finditer(strip_inline_code_spans(line)):
            refs.setdefault(ref.group(1), []).append(lineno)

    missing = {
        key: refs[key]
        for key in sorted(set(refs) - set(defs), key=sort_key)
    }
    unused = {
        key: defs[key]
        for key in sorted(set(defs) - set(refs), key=sort_key)
    }
    duplicate_defs = {
        key: lines
        for key, lines in sorted(defs.items(), key=lambda item: sort_key(item[0]))
        if len(lines) > 1
    }

    failed = bool(missing or duplicate_defs or (unused and not allow_unused))
    return {
        "path": str(path),
        "status": "fail" if failed else "pass",
        "references": refs,
        "definitions": defs,
        "missing_definitions": missing,
        "unused_definitions": unused,
        "duplicate_definitions": duplicate_defs,
    }


def sort_key(value: str) -> tuple[int, int | str]:
    return (0, int(value)) if value.isdigit() else (1, value)


def resolve_paths(paths: list[str], extensions: tuple[str, ...]) -> list[Path]:
    resolved: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(raw)
        if path.is_dir():
            resolved.extend(
                sorted(p for p in path.rglob("*") if p.is_file() and p.suffix in extensions)
            )
        elif path.suffix in extensions:
            resolved.append(path)
    return resolved


def print_human(results: list[dict]) -> None:
    for result in results:
        print(f"{result['status'].upper()} {result['path']}")
        for label, title in (
            ("missing_definitions", "missing definitions"),
            ("unused_definitions", "unused definitions"),
            ("duplicate_definitions", "duplicate definitions"),
        ):
            items = result[label]
            if not items:
                continue
            print(f"  {title}:")
            for key, lines in items.items():
                joined = ", ".join(str(line) for line in lines)
                print(f"    [^{key}] lines {joined}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Check Markdown footnote references have matching definitions."
    )
    parser.add_argument("paths", nargs="+", help="Markdown files or directories to check.")
    parser.add_argument(
        "--allow-unused",
        action="store_true",
        help="Do not fail when a footnote definition has no matching reference.",
    )
    parser.add_argument(
        "--extensions",
        default=".md,.mdx",
        help="Comma-separated extensions to scan when a directory is passed.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args(argv)

    extensions = tuple(ext.strip() for ext in args.extensions.split(",") if ext.strip())
    try:
        paths = resolve_paths(args.paths, extensions)
    except FileNotFoundError as exc:
        print(f"missing path: {exc}", file=sys.stderr)
        return 2

    if not paths:
        print("no Markdown files matched", file=sys.stderr)
        return 2

    results = [analyze_file(path, args.allow_unused) for path in paths]
    payload = {
        "status": "fail" if any(result["status"] == "fail" for result in results) else "pass",
        "checked_files": len(results),
        "results": results,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_human(results)

    return 1 if payload["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
