#!/bin/bash
# PreToolUse hook: blocks dangerous git commands.
#
# FAILS CLOSED. A guardrail whose failure mode is silence is worse than no
# guardrail, because it is trusted: if jq is missing, or the payload shape
# changes so the command can't be extracted, the old version matched nothing
# and exited 0 — silently permitting every command it exists to block.
# Exit 2 = block (per Claude Code hook contract).

if ! command -v jq >/dev/null 2>&1; then
  echo "BLOCKED: git-guardrails hook cannot run — jq is not installed. Refusing to allow git commands unchecked. Install jq or remove this hook." >&2
  exit 2
fi

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  echo "BLOCKED: git-guardrails hook could not extract the command from the hook payload (shape changed?). Refusing to allow it unchecked." >&2
  exit 2
fi

DANGEROUS_PATTERNS=(
  "git push"
  "git reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \."
  "git restore \."
  "push --force"
  "reset --hard"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches dangerous pattern '$pattern'. The user has prevented you from doing this." >&2
    exit 2
  fi
done

exit 0
