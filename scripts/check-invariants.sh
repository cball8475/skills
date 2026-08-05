#!/usr/bin/env bash
set -euo pipefail

# Enforces the repo invariants documented in CLAUDE.md. Run locally or in CI.
# These rules existed only as prose before, and drifted silently (all four
# misc/ skills were missing from plugin.json with nothing to notice).
#
#   1. Every skill in engineering/, productivity/, or misc/ is referenced in
#      the top-level README.md (linked to its SKILL.md) and listed in
#      .claude-plugin/plugin.json.
#   2. Skills in personal/, in-progress/, and deprecated/ appear in NEITHER.
#   3. Each bucket README (engineering/, productivity/, misc/) links every
#      skill in its bucket to its SKILL.md.
#   4. The banned-word mirror in EATON/CLAUDE.md still matches the Tier 1 and
#      Personal Tier 1 tables in avoid-ai-writing. Runs only when EATON is
#      checked out beside this repo, so CI skips it; see check-mirror.py.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

fail=0
err() { echo "✗ $1" >&2; fail=1; }

PLUGIN=.claude-plugin/plugin.json

# jq is required to parse plugin.json — fail loudly, not by skipping checks.
command -v jq >/dev/null 2>&1 || { echo "✗ jq is required to run this check" >&2; exit 1; }

# ── Promoted buckets: must be everywhere ──
for bucket in engineering productivity misc; do
  for dir in skills/$bucket/*/; do
    [ -f "$dir/SKILL.md" ] || continue
    name="$(basename "$dir")"
    rel="skills/$bucket/$name"

    grep -q "$rel/SKILL.md" README.md ||
      err "$rel: no SKILL.md link in top-level README.md"

    jq -e --arg p "./$rel" '.skills | index($p)' "$PLUGIN" >/dev/null ||
      err "$rel: missing from $PLUGIN"

    grep -q "$name/SKILL.md" "skills/$bucket/README.md" ||
      err "$rel: not linked in skills/$bucket/README.md"
  done
done

# ── Unpromoted buckets: must be nowhere ──
for bucket in personal in-progress deprecated; do
  [ -d "skills/$bucket" ] || continue
  for dir in skills/$bucket/*/; do
    [ -f "$dir/SKILL.md" ] || continue
    name="$(basename "$dir")"
    rel="skills/$bucket/$name"

    ! grep -q "$rel" README.md ||
      err "$rel: $bucket/ skills must not appear in top-level README.md"

    ! jq -e --arg p "./$rel" '.skills | index($p)' "$PLUGIN" >/dev/null ||
      err "$rel: $bucket/ skills must not appear in $PLUGIN"
  done
done

# ── plugin.json must not reference skills that don't exist ──
while IFS= read -r entry; do
  [ -f "${entry#./}/SKILL.md" ] ||
    err "$PLUGIN references $entry but ${entry#./}/SKILL.md does not exist"
done < <(jq -r '.skills[]' "$PLUGIN")

# ── Banned-word mirror in EATON/CLAUDE.md ──
# Skips with a notice when EATON is not beside this repo, which is the case in
# CI. That makes this a local gate, not a CI gate: run it before committing a
# change to the Tier 1 or Personal Tier 1 tables.
if command -v python3 >/dev/null 2>&1; then
  python3 scripts/check-mirror.py || err "banned-word mirror drift — see above"
else
  echo "- mirror check skipped: python3 not available"
fi

if [ "$fail" -ne 0 ]; then
  echo "" >&2
  echo "CLAUDE.md invariants violated — see above." >&2
  exit 1
fi
echo "✓ all CLAUDE.md invariants hold"
