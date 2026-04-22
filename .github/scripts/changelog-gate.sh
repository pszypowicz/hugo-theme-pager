#!/usr/bin/env bash
#
# Decide whether a pull_request must update CHANGELOG.md.
#
# Prints `true` to stdout if the PR must update CHANGELOG (theme-behavior
# files touched AND no escape hatch set), or `false` otherwise. Diagnostic
# output goes to stderr so stdout is clean for capture.
#
# Intended to run from a GitHub Actions step whose env passes the PR base
# and head SHAs, the PR body, and the JSON-encoded list of label names.
# Usable locally too: set the same env vars, run the script.

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: BASE_SHA=... HEAD_SHA=... [PR_BODY=...] [PR_LABELS=...] changelog-gate.sh

Prints `true` if the PR must update CHANGELOG.md, `false` otherwise.
Diagnostics are written to stderr.

Environment variables:
  BASE_SHA   PR base commit SHA (required).
  HEAD_SHA   PR head commit SHA (required).
  PR_BODY    PR description text (default: empty).
  PR_LABELS  JSON array of label names, e.g. '["skip-changelog"]'
             (default: '[]').

Escape hatches (set via PR metadata, not the script):
  - Add the `skip-changelog` label to the PR, OR
  - Include `[skip changelog]` anywhere in the PR body.

Exit codes:
  0  Decision written to stdout.
  2  Missing required env var or unknown CLI flag.
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

: "${BASE_SHA:?BASE_SHA not set}"
: "${HEAD_SHA:?HEAD_SHA not set}"
PR_BODY="${PR_BODY:-}"
PR_LABELS="${PR_LABELS:-[]}"

if printf '%s' "$PR_LABELS" | grep -q '"skip-changelog"'; then
  echo "skip-changelog label set; CHANGELOG update not required." >&2
  echo false
  exit 0
fi

if printf '%s' "$PR_BODY" | grep -Fq '[skip changelog]'; then
  echo "[skip changelog] present in PR body; CHANGELOG update not required." >&2
  echo false
  exit 0
fi

git fetch --no-tags origin "$BASE_SHA" "$HEAD_SHA" >/dev/null 2>&1 || true

changed=$(git diff --name-only "$BASE_SHA" "$HEAD_SHA")
printf 'Files changed in this PR:\n%s\n\n' "$changed" >&2

# Paths that do NOT by themselves require a CHANGELOG entry. Everything
# else (assets/, layouts/, static/, theme.toml, go.mod, exampleSite/, etc.)
# counts as user-visible and triggers the requirement.
ignored_re='^(CHANGELOG\.md|README\.md|LICENSE|\.gitignore|\.gitattributes|\.github/|images/)'

needs_entry=false
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if ! printf '%s' "$f" | grep -Eq "$ignored_re"; then
    needs_entry=true
    break
  fi
done <<< "$changed"

if [ "$needs_entry" = "false" ]; then
  echo "Only docs / CI / meta files changed; CHANGELOG update not required." >&2
  echo false
else
  echo "PR touches theme behavior; CHANGELOG update required." >&2
  echo true
fi
