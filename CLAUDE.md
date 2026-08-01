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
- `scripts/link-skills.sh` — symlinks every non-deprecated skill into `~/.claude/skills` for the local CLI. Takes optional extra root directories as arguments, for skills kept outside this repo.
- `scripts/list-skills.sh` — lists every `SKILL.md` path in the repo.
