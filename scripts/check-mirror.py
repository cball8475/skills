#!/usr/bin/env python3
"""Verify that the EATON/CLAUDE.md banned-word mirror still matches this skill.

    python3 scripts/check-mirror.py [--claude-md PATH] [--require]

The word list has one home: the Tier 1 and Personal Tier 1 tables in
`skills/productivity/avoid-ai-writing/SKILL.md`. `EATON/CLAUDE.md` carries an
inline mirror of it, because that file is the only thing a Claude session loads
automatically and this repo is not attached to every session. A mirror that
nobody checks is a copy that drifts, which is the problem the single source was
supposed to end, so this script checks it.

Two invariants, one in each direction:

  A. Every word in the CLAUDE.md mirror is covered by the skill's tables.
     Catches a word being dropped or reworded here while CLAUDE.md keeps
     promising it is enforced.
  B. Every Personal Tier 1 entry appears in the CLAUDE.md mirror.
     Catches a personal ban added here and never mirrored, which would apply
     when the skill happens to be loaded and silently not otherwise.

Exit 0 when both hold. Exit 1 on drift, listing the terms in both directions.

CLAUDE.md is found via --claude-md, then the EATON_CLAUDE_MD environment
variable, then the usual sibling checkouts. When it cannot be found the check
is SKIPPED and still exits 0, so this repo's CI (where EATON is not checked
out) stays green. Pass --require to make a missing file a failure instead.
"""

import argparse
import os
import re
import sys
from pathlib import Path

SKILL_REL = "skills/productivity/avoid-ai-writing/SKILL.md"

CLAUDE_MD_ENV = "EATON_CLAUDE_MD"
CLAUDE_MD_CANDIDATES = [
    "../EATON/CLAUDE.md",
    "../eaton/CLAUDE.md",
    "~/EATON/CLAUDE.md",
    "~/projects/eaton-ehs-project/CLAUDE.md",
]

# Headings whose first column holds always-replace vocabulary.
TIER1_HEADING = "tier 1"
PERSONAL_HEADING = "personal tier 1"

# Any "**Banned <something> (mirror):**" line counts, so the mirror can be split
# across several lines (words, steering frames) without this going blind to one.
MIRROR_RE = re.compile(r"^\*\*Banned [^:*]*\(mirror\):\*\*\s*(.+)$", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
PARENTHETICAL_RE = re.compile(r"\([^)]*\)")


def normalize(term):
    """Reduce a table cell or mirror entry to comparable bare terms.

    Strips the qualifiers that exist for human readers -- "(metaphor)",
    "(as in 'the EHS space')", markdown emphasis -- and splits the slash-
    separated variants a single table row can carry.
    """
    term = PARENTHETICAL_RE.sub(" ", term)
    term = term.replace("*", " ").replace("`", " ").replace("…", " ")
    variants = []
    for part in term.split("/"):
        part = " ".join(part.split()).strip().lower()
        if part and re.search(r"[a-z]", part):
            variants.append(part)
    return variants


def parse_tables(skill_path):
    """Return (tier1_variants, personal_entries).

    tier1_variants is the flat set of every bare term in Tier 1 and Personal
    Tier 1. personal_entries keeps the rows grouped, so invariant B can accept
    any one variant of a multi-variant row.
    """
    all_variants = set()
    personal_entries = []
    section = None

    for line in skill_path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^#{2,4}\s+(.*)$", line)
        if heading:
            title = heading.group(1).strip().lower()
            if title.startswith(PERSONAL_HEADING):
                section = "personal"
            elif title.startswith(TIER1_HEADING):
                section = "tier1"
            else:
                section = None
            continue
        if section is None:
            continue

        row = TABLE_ROW_RE.match(line)
        if not row:
            continue
        cell = row.group(1).split("|")[0].strip()
        if not cell or cell.lower() == "replace" or set(cell) <= set("-: "):
            continue

        variants = normalize(cell)
        if not variants:
            continue
        all_variants.update(variants)
        if section == "personal":
            personal_entries.append((cell, variants))

    return all_variants, personal_entries


def parse_mirror(claude_md_path):
    text = claude_md_path.read_text(encoding="utf-8")
    matches = MIRROR_RE.findall(text)
    if not matches:
        raise SystemExit(
            "error: no '**Banned ... (mirror):**' line in {}.\n"
            "The mirror is what this check compares against; if it was renamed, "
            "update MIRROR_RE here too.".format(claude_md_path))
    entries = []
    for line in matches:
        for raw in line.split(","):
            variants = normalize(raw)
            if variants:
                entries.append((" ".join(raw.split()).strip(), variants[0]))
    return entries


def find_claude_md(explicit, repo):
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise SystemExit("error: --claude-md {} is not a file".format(explicit))
        return path
    candidates = []
    if os.environ.get(CLAUDE_MD_ENV):
        candidates.append(Path(os.environ[CLAUDE_MD_ENV]).expanduser())
    for rel in CLAUDE_MD_CANDIDATES:
        candidates.append((repo / rel).expanduser() if rel.startswith(".")
                          else Path(rel).expanduser())
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved.is_file():
            return resolved
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--claude-md", metavar="PATH",
                        help="path to EATON/CLAUDE.md holding the mirror")
    parser.add_argument("--require", action="store_true",
                        help="fail if CLAUDE.md cannot be found, instead of skipping")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent.parent
    skill_path = repo / SKILL_REL
    if not skill_path.is_file():
        raise SystemExit("error: {} not found".format(skill_path))

    claude_md = find_claude_md(args.claude_md, repo)
    if claude_md is None:
        message = ("mirror check SKIPPED: no EATON CLAUDE.md found. Pass "
                   "--claude-md PATH or set {}.".format(CLAUDE_MD_ENV))
        if args.require:
            print("✗ " + message.replace("SKIPPED", "FAILED"), file=sys.stderr)
            return 1
        print("- " + message)
        return 0

    table_variants, personal_entries = parse_tables(skill_path)
    mirror = parse_mirror(claude_md)
    mirror_variants = {variant for _, variant in mirror}

    uncovered = [display for display, variant in mirror
                 if variant not in table_variants]
    unmirrored = [display for display, variants in personal_entries
                  if not any(v in mirror_variants for v in variants)]

    if uncovered or unmirrored:
        print("✗ banned-word mirror has drifted from {}".format(SKILL_REL),
              file=sys.stderr)
        for display in uncovered:
            print("  in the CLAUDE.md mirror but not in Tier 1 or Personal Tier 1: "
                  "{}".format(display), file=sys.stderr)
        for display in unmirrored:
            print("  in Personal Tier 1 but not in the CLAUDE.md mirror: "
                  "{}".format(display), file=sys.stderr)
        print("", file=sys.stderr)
        print("The skill is canonical. Fix the mirror in {} to match, or change "
              "the tables here deliberately and mirror the change.".format(claude_md),
              file=sys.stderr)
        return 1

    print("✓ mirror matches: {} words in {}, all covered; {} Personal Tier 1 "
          "entries, all mirrored".format(len(mirror), claude_md.name,
                                         len(personal_entries)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
