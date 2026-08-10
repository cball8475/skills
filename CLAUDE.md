# CLAUDE.md

This repo is a personal fork of [mattpocock/skills](https://github.com/mattpocock/skills): a collection of Claude Code skills, shipped as a plugin via `.claude-plugin/plugin.json` and documented in the top-level `README.md`.

## Layout

Skills live in bucket folders under `skills/`, one folder per skill, each containing a `SKILL.md`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `misc/` — kept around but rarely used
- `personal/` — tied to my own setup, not promoted
- `in-progress/` — drafts not yet ready to ship
- `deprecated/` — no longer used

`engineering/`, `productivity/`, and `misc/` are the **promoted** buckets — their skills ship in the plugin. `personal/`, `in-progress/`, and `deprecated/` are **unpromoted**.

## Invariants (enforced by CI)

`scripts/check-invariants.sh` enforces these rules; CI runs it on every push and PR. Run it locally before committing any change that adds, moves, renames, or removes a skill:

1. Every skill in a promoted bucket has an entry in the top-level `README.md` (skill name linked to its `SKILL.md`) and an entry in `.claude-plugin/plugin.json`.
2. Skills in unpromoted buckets appear in **neither** the top-level `README.md` nor `plugin.json`.
3. Every bucket `README.md` lists each skill in its bucket with a one-line description, with the skill name linked to its `SKILL.md`.
4. Every `plugin.json` entry points at a directory that actually contains a `SKILL.md`.
5. The banned-word mirror in `EATON/CLAUDE.md` matches the **Tier 1** and **Personal Tier 1** tables in `avoid-ai-writing`: every mirrored word is covered by the tables, and every Personal Tier 1 entry is mirrored.

Invariant 5 is a **local** gate, not a CI one. EATON is a separate private repo and is not checked out in CI, so the check skips there with a notice. Run `bash scripts/check-invariants.sh` with both repos present before committing any change to those two tables — the mirror exists because `EATON/CLAUDE.md` is the only file a Claude session auto-loads, and a mirror nobody checks is exactly the drift the single source was meant to end.

## Adding, moving, or retiring a skill

- **New skill**: create `skills/<bucket>/<name>/SKILL.md`, add an entry to that bucket's `README.md`, and — if the bucket is promoted — to the top-level `README.md` Reference section and `plugin.json`.
- **Bucket README entry format**: `- **[name](./name/SKILL.md)** — one-line description.`
- **Moving a skill between buckets**: update both bucket READMEs, and add or remove the top-level `README.md` and `plugin.json` entries to match the destination bucket's promotion status.
- **Retiring a skill**: move it to `deprecated/` (don't delete it), then remove its promoted-bucket references.
- Finish with `bash scripts/check-invariants.sh`.

## Supporting docs

- `CONTEXT.md` — the repo's shared language (**Issue tracker**, **Issue**, **Triage role**). Use these terms, and their listed avoid-words, consistently in skills and docs.
- `docs/adr/` — architecture decision records for skill-design conventions (e.g. when a skill should point at `/setup-matt-pocock-skills` explicitly). Check them before changing how skills are structured.
- `.out-of-scope/` — features that were considered and deliberately declined, with reasons. Check here before proposing or implementing a feature request; if it's listed, don't build it.

## Scripts

- `scripts/check-invariants.sh` — the invariant checker above (requires `jq`).
- `scripts/check-mirror.py` — invariant 5 on its own. Finds `EATON/CLAUDE.md` via `--claude-md`, the `EATON_CLAUDE_MD` environment variable, or the usual sibling checkouts; skips with exit 0 when it finds none, or fails on that with `--require`.
- `scripts/link-skills.sh` — symlinks every non-deprecated skill into `~/.claude/skills` for the local CLI. Takes optional extra root directories as arguments, for skills kept outside this repo.
- `scripts/list-skills.sh` — lists every `SKILL.md` path in the repo.

## Agent Fleet

`.claude/agents/` holds read-only subagent definitions for auditing this repo's
30 skills. Per-skill review is wide and independent — 30 items, each judgeable
on its own — which is the shape fan-out is for.

**These are not skills, and they are deliberately outside both promotion
systems.** They live in `.claude/agents/` at the repo root, not in a bucket, and
they are not in `.claude-plugin/plugin.json`. Three reasons, in order:

1. A bucket placement would put them under `skills/<bucket>/` and trip
   invariants 1–3, which expect a `SKILL.md` and a README entry.
2. Promoting them would ship repo-maintenance tooling to everyone who installs
   the plugin. They audit *this* repo and are useless anywhere else.
3. Putting them in an unpromoted bucket to dodge invariant 1 would be filing
   them as a kind of thing they are not.

`scripts/check-invariants.sh` only walks `skills/<bucket>/*/`, so `.claude/`
is invisible to it and the promoted/unpromoted rules are untouched. Verified
green on 2026-08-10 with the fleet in place.

### Doctrine

**Agents read, Charlie approves, the main session writes.** Every agent is
read-only: no edits, no commits. That is what makes fan-out safe — read-only
agents cannot overwrite each other, so all 30 can run at once.

**One job per agent, scoped to one skill.** Fan-out comes from spawning N
agents, not from handing one agent the skill list.

**Every agent file restates the rules it depends on.** No agent inherits this
file. The read-only rule, ADR 0001's soft-dependency split, and the
`avoid-ai-writing` prohibition are written into each definition.

**Documented false positives live in the file**, dated, derived from real runs.

**Structured output block at the end of every definition**, so 30 results read
side by side.

**Findings go through `finding-verifier`** before Charlie sees them. It defaults
to `REFUTED`, and it may run `check-invariants.sh` to refute a structural claim.

**No agent duplicates the script.** `check-invariants.sh` owns the structural
rules mechanically and in CI. Agents cover only what a script cannot judge:
whether a description would trigger correctly, whether a body contradicts
itself, whether two skills collide.

### The agents

| Agent | Item | Reports |
|---|---|---|
| `skill-auditor` | one skill | description accuracy, internal contradiction, dead references, `CONTEXT.md` vocabulary, bucket fit |
| `skill-overlap-checker` | one skill | trigger collisions against every other description |
| `finding-verifier` | one finding | `CONFIRMED` / `REFUTED` / `UNVERIFIABLE` |

### When to fan out, when to single-thread

**Fan out** when the items are independent and nothing writes: auditing every
skill, checking every description for collisions, verifying a set of findings.

**Single-thread** when steps depend on each other or when anything writes. Every
skill edit, every bucket move, every `plugin.json` change and every commit stays
sequential and stays in the main session — a bucket move touches three files
that have to agree, and `check-invariants.sh` is the gate on all of it.

### Watch the first minute

Read the opening of a run before stepping away — whether the agent read the
skill it was given and checked ADR 0001 and `.out-of-scope/` before judging.
Signals worth catching early: work on a skill nobody asked about, findings that
restate what `check-invariants.sh` already covers, scope widening past the one
skill it was given.

### The banned-word list is off-limits to agents

The **Tier 1** and **Personal Tier 1** tables in
`skills/productivity/avoid-ai-writing/SKILL.md` are the canonical list for three
repos: this one, the mirror in `EATON/CLAUDE.md` (checked by
`scripts/check-mirror.py`), and `check_voice.py` in `before-human-error`, which
parses those tables live at runtime and keeps no copy of its own. An agent may
report drift in them. No agent edits them, and no agent picks a winner between
two versions.
