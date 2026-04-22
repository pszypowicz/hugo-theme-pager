#!/usr/bin/env python3
"""
Validate CHANGELOG.md against the project's conventions.

Structural checks (always run):
  - File is non-empty and ends with a trailing newline.
  - Every `## [...]` heading has a blank line before and after it.
  - At most one `## [Unreleased]` heading exists in the file.
  - If `## [Unreleased]` exists, no version heading precedes it.
  - Every non-Unreleased `## [...]` heading matches `## [X.Y.Z]` exactly
    (no dates: git tags carry those).
  - Version headings appear in strictly descending semver order.

Diff checks (run only when --base-sha / --head-sha are supplied):
  - The CHANGELOG was modified in the PR, AND
  - The modification either extended the `## [Unreleased]` section OR
    introduced a new `## [X.Y.Z]` heading that was absent at the base commit.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

H2_LOOSE = re.compile(r"^##\s")
H2_RE = re.compile(r"^## \[(?P<name>[^\]]+)\]\s*$")
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def parse_sections(text: str):
    """Return a list of dicts describing each `## [...]` section.

    Each section carries: 1-based line number, heading name, optional date,
    and the list of body lines up to (but not including) the next H2.
    """
    lines = text.split("\n")
    sections = []
    current = None
    for i, line in enumerate(lines):
        m = H2_RE.match(line)
        if m:
            if current is not None:
                sections.append(current)
            current = {
                "line": i + 1,
                "name": m.group("name"),
                "body": [],
            }
        elif current is not None:
            current["body"].append(line)
    if current is not None:
        sections.append(current)
    return sections


def version_tuple(name: str):
    m = SEMVER_RE.match(name)
    return tuple(int(p) for p in m.groups()) if m else None


def check_structure(text: str, path: str) -> list[str]:
    errors: list[str] = []

    if not text:
        return [f"{path} is empty"]
    if not text.endswith("\n"):
        errors.append(f"{path} does not end with a trailing newline")

    lines = text.split("\n")
    for i, line in enumerate(lines):
        if not H2_LOOSE.match(line):
            continue
        if not H2_RE.match(line):
            errors.append(
                f"{path}:{i + 1}: `{line.strip()}` does not match `## [Unreleased]` "
                "or `## [X.Y.Z]` (dates are not tracked in the changelog)"
            )
            continue
        if i > 0 and lines[i - 1].strip() != "":
            errors.append(f"{path}:{i + 1}: `{line.strip()}` is not preceded by a blank line")
        if i + 1 < len(lines) and lines[i + 1].strip() != "":
            errors.append(f"{path}:{i + 1}: `{line.strip()}` is not followed by a blank line")

    sections = parse_sections(text)

    unreleased = [s for s in sections if s["name"] == "Unreleased"]
    if len(unreleased) > 1:
        locations = ", ".join(f"line {s['line']}" for s in unreleased)
        errors.append(
            f"{path}: multiple `## [Unreleased]` headings found ({locations}); only one is allowed"
        )

    if unreleased:
        first_versioned = next((s for s in sections if s["name"] != "Unreleased"), None)
        if first_versioned is not None and unreleased[0]["line"] > first_versioned["line"]:
            errors.append(
                f"{path}:{unreleased[0]['line']}: `## [Unreleased]` appears below version "
                f"`[{first_versioned['name']}]` (line {first_versioned['line']}); "
                "`[Unreleased]` must precede all versioned entries"
            )

    versioned = [s for s in sections if s["name"] != "Unreleased"]
    for s in versioned:
        if not SEMVER_RE.match(s["name"]):
            errors.append(
                f"{path}:{s['line']}: `[{s['name']}]` is not a valid semver (X.Y.Z)"
            )

    prev = None
    for s in versioned:
        v = version_tuple(s["name"])
        if v is None:
            continue
        if prev is not None and v >= prev["version"]:
            errors.append(
                f"{path}:{s['line']}: version `[{s['name']}]` is not strictly less than "
                f"preceding `[{prev['name']}]` (line {prev['line']}); "
                "version headings must appear newest-first"
            )
        prev = {"version": v, "name": s["name"], "line": s["line"]}

    return errors


def git_show(sha: str, path: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "show", f"{sha}:{path}"], stderr=subprocess.DEVNULL
        ).decode()
    except subprocess.CalledProcessError:
        return None


def check_diff(base_sha: str, head_sha: str, path: str) -> list[str]:
    base_text = git_show(base_sha, path)
    head_text = git_show(head_sha, path)

    if head_text is None:
        return [f"{path} does not exist at HEAD ({head_sha})"]
    if base_text is None:
        base_text = ""

    if base_text == head_text:
        return [
            f"{path} was not modified between {base_sha[:7]} and {head_sha[:7]}; "
            "expected either a new `## [X.Y.Z]` heading or additional "
            "content under `## [Unreleased]`"
        ]

    base_sections = parse_sections(base_text)
    head_sections = parse_sections(head_text)

    base_versions = {s["name"] for s in base_sections if s["name"] != "Unreleased"}
    head_versions = {s["name"] for s in head_sections if s["name"] != "Unreleased"}
    new_versions = head_versions - base_versions
    if new_versions:
        return []

    base_unreleased = next((s for s in base_sections if s["name"] == "Unreleased"), None)
    head_unreleased = next((s for s in head_sections if s["name"] == "Unreleased"), None)
    base_body = base_unreleased["body"] if base_unreleased else None
    head_body = head_unreleased["body"] if head_unreleased else None
    if base_body != head_body:
        return []

    return [
        f"{path} was modified but neither extended `## [Unreleased]` nor introduced "
        "a new version heading. Put new entries under `## [Unreleased]`, or add a "
        "`## [X.Y.Z]` section immediately above it."
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True, help="Path to CHANGELOG.md")
    ap.add_argument("--base-sha", help="Base commit SHA for diff check")
    ap.add_argument("--head-sha", help="Head commit SHA for diff check")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as f:
        text = f.read()

    errors = check_structure(text, args.file)

    if (args.base_sha is None) ^ (args.head_sha is None):
        print("::error::--base-sha and --head-sha must be provided together", file=sys.stderr)
        return 2
    if args.base_sha and args.head_sha:
        errors.extend(check_diff(args.base_sha, args.head_sha, args.file))

    if errors:
        for e in errors:
            print(f"::error::{e}")
        return 1

    mode = "structure + diff" if args.base_sha else "structure"
    print(f"{args.file} validation passed ({mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
