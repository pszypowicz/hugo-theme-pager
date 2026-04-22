#!/usr/bin/env python3
"""
Extract the body of a single `## [X.Y.Z]` section from CHANGELOG.md.

Prints the section body to stdout (bullets and subheadings, with leading
and trailing blank lines trimmed). Exits nonzero with a `::error::`
annotation if the requested version has no matching heading.

Usage:
  extract-changelog-section.py --file CHANGELOG.md --version 0.2.0
"""

from __future__ import annotations

import argparse
import re
import sys

H2_RE = re.compile(r"^## \[(?P<name>[^\]]+)\]\s*$")
LINK_REF_RE = re.compile(r"^\[[^\]]+\]:\s+\S+")


def extract(text: str, version: str) -> str | None:
    body: list[str] = []
    in_section = False
    for line in text.split("\n"):
        m = H2_RE.match(line)
        if m:
            if in_section:
                break
            if m.group("name") == version:
                in_section = True
            continue
        if in_section:
            body.append(line)
    if not in_section:
        return None
    # Drop markdown link-reference lines (`[foo]: https://...`); they're
    # only meaningful within the full CHANGELOG and would render as noise
    # in a standalone release body.
    body = [ln for ln in body if not LINK_REF_RE.match(ln)]
    while body and body[0].strip() == "":
        body.pop(0)
    while body and body[-1].strip() == "":
        body.pop()
    return "\n".join(body)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True)
    ap.add_argument("--version", required=True, help="e.g. 0.2.0 (no leading `v`)")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as f:
        text = f.read()

    body = extract(text, args.version)
    if body is None:
        print(
            f"::error::no `## [{args.version}]` section in {args.file}",
            file=sys.stderr,
        )
        return 1
    if not body.strip():
        print(
            f"::error::`## [{args.version}]` section in {args.file} is empty",
            file=sys.stderr,
        )
        return 1
    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
