---
name: before-human-error
description: >-
  Autonomously produces the weekly "Before Human Error" incident-teardown
  newsletter end to end, for Charlie to review and approve. Triggered when
  Charlie names an incident (preferred) or says "write article #N": confirms
  the target incident, runs the mandatory Positioning Pass, drafts a
  multi-source fact-checked teardown in the house voice, runs the de-AI pass,
  saves ONE canonical doc to Google Drive for review, and stages the LinkedIn
  (full post) + beehiiv publication. Publishing is manual; Charlie supervises
  and posts. Maintains a 2-3 issue buffer. Scheduled-session launcher prompts
  live in PROMPTS.md next to this file.
---

# Before Human Error — weekly teardown pipeline

## Operating rules (read D1 first)
- DB: `before-human-error` (D1 id `06f4ca9c-7089-434b-a34a-b4c4803d23a7`).
- Before anything, read `project_state` (operating_model_v2, cadence,
  source_policy) and `operating_guide` (GUARDRAILS first, then Decision
  Principle, voice, Positioning Pass, Sourcing & Fact Discipline, LinkedIn
  Posting Playbook, latest market scan). D1 is the source of truth and may be
  newer than this file.
- IF D1 IS UNREACHABLE after retries: HALT and report the outage to Charlie.
  NEVER run the pipeline from memory or from this file alone — verify-before-
  assert is unenforceable without the live database. If connectivity drops
  MID-run, re-read the rows you depend on before any further writes.
- TRIGGER: Charlie names the incident ("write the Tesoro Anacortes article")
  or says "write article #N". Numbers drift (issues get renumbered), so BEFORE
  drafting, resolve the target against `issues`/`incidents` and confirm in one
  line: "Article N = <incident name>, <hazard> — correct?" If the reference is
  ambiguous or matches nothing, STOP and ask; never guess the target article.
  Publishing is MANUAL — Charlie posts; this skill only drafts + stages. Never
  publish or schedule anything yourself.
- Cadence: WEEKLY, publish Tuesday. LinkedIn is the primary channel; beehiiv is
  secondary while the list is tiny. Keep a 2-3 issue buffer.
- Charlie = approve, review & publish. Always explain the reasoning behind any
  recommendation.
- Scheduled-session launcher prompts (Friday draft / Monday report) are
  versioned in `PROMPTS.md` in this folder — the only copy. Do not maintain
  prompt copies in Drive; they drift.

## Step 0 — GUARDRAILS GATE (non-negotiable; full text in operating_guide "GUARDRAILS")
Purpose: stop the recurring failure of stating stale/assumed info as current
fact and letting one data point become a rule. Apply on every run:
1. VERIFY BEFORE ASSERT — re-check every changeable fact (issue/incident status,
   who replied, subscriber/analytics numbers, dates, what is published) against
   its LIVE source this run; never state it from memory. Label anything you
   cannot verify as "per memory, unverified."
2. RECONCILE CONTRADICTIONS — if two records disagree, stop and resolve before
   reporting; never report the convenient one. TRIPWIRE: if two non-superseded
   `issues` rows share a number, stop and reconcile with Charlie before
   anything else.
3. ONE DATA POINT IS NOT A RULE — conclusions stay hypotheses with their
   evidence and sample size; re-derive from current numbers each run.
4. STABLE KEYS — reference incidents and sponsors by name or hazard type, never
   by issue number.
5. ONE SOURCE OF TRUTH — D1 is canonical (read first); ONE Google Doc per issue;
   `main` is the only repo truth. No duplicates that can drift.

Before handing Charlie ANYTHING to publish, or any status report, the GATE
(all must be YES):
[ ] claims 2-sourced or labeled unverified
[ ] statuses and numbers re-checked against the live source THIS run
[ ] assumptions / `[NEEDS INPUT]` flagged to Charlie
[ ] one canonical doc, no scratch duplicates
[ ] issue folder complete: canonical doc + `sources/` (primary report staged
    or an explicit pointer to its archive path) + `figures/`
If any is NO, fix it or flag it before shipping.

## HARD RULES (non-negotiable)
1. **No assumptions when the fact is obtainable. Sources are GLOBAL, not
   US-only.** The CSB + the Drive incident archive are a primary backbone, but
   incidents and corroborating facts may come from anywhere: US (NTSB, OSHA,
   NIOSH FACE, EPA), UK (HSE, public inquiries), EU (Seveso/eMARS), Australia
   (royal commissions, ATSB), Canada (TSB), journals (IChemE Loss Prevention
   Bulletin), standards bodies, and contemporaneous news. If the primary report
   is silent, GO RESEARCH the fact and cite the corroborating source. Do not
   assume; do not flag-and-skip.
2. **Cite 2+ independent sources every issue. Never single-source.**
3. Only mark `[NEEDS INPUT]` for a fact genuinely unobtainable after a real
   search, and surface it to Charlie at review.
4. Run the de-AI pass; match the house voice exactly.

## Sourcing readiness (operational — separate from editorial scope)
Editorial scope is GLOBAL. The only operational requirement is that an
incident's PRIMARY source be reachable by an unattended run. An incident is
`auto-ready` when its primary report is staged in the Drive archive OR is
reachable on the open web. As of 2026-06-28 the network policy was widened and
WebFetch works (verified live against csb.gov), so arbitrary web fetch is no
longer blocked — fetch primary reports live when needed. The Drive CSB archive
remains the durable fallback (and the fastest path), so prefer it when a report
is already staged. For a `pending-source` incident whose primary report is not
staged and not easily fetchable, stage the primary report in Drive first, or
handle it as a supervised special. Never let any egress limit shrink the
editorial scope — stage the source instead.

### Drive CSB archive layout (where staged reports live)
- Folder: `Before Human Error / CSB Archive /`.
  - `reports/<csb_id>_<slug>/` — one folder per completed CSB investigation
    (the full final-report PDF[s]). This path is stored in `incidents.report_path`
    as `CSB Archive/reports/<csb_id>_<slug>` for every `auto-ready` CSB incident.
  - `summaries/volume_N_<date>.pdf` — the four CSB "Incident Reports" volumes
    (~94 shorter accidental-release events) for lighter-weight teardowns.
  - `csb-archive-catalog.csv` — the full ~131-investigation index (name,
    location, final-report date, detail URL, csb_id) for picking the next
    incident and resolving its `report_path`.

## Step 1 — Positioning Pass (GATE; output written at top of draft)
Do not write the body until 1-3 are answered in writing.
1. Incident coverage scan — who already told this story; the dominant "easy
   story" to dismantle (don't just echo existing coverage).
2. Angle differentiation — the one insight this issue owns (one sentence).
3. Amplify lever (per latest market scan): engineering specificity (vs
   philosophy/HOP voices) / voice & narrative (vs dry institutional) /
   white-space medium (companion video or carousel).
4. Sponsor match — vendor category fitting this incident -> log to `sponsors`.
5. Leading-indicator beat — the ignored near-miss / missed warning (the hook).
6. Hook + subject — feed-teaser first two lines (hard curiosity gap) +
   "blamed X / the report said Y" subject line.

## Step 2 — Draft (house structure)
Cold Open -> How the Unit Worked -> What Happened -> The Easy Story ->
What Actually Set It Up -> How They Got Past Human Error -> The Gap ->
Monday Morning Checklist -> Landing Line -> Footer + sources.
Vary the closing "you don't need X, you need Y" line so the template doesn't show.

### Voice
First person, plain, declarative. Concede the obvious before reframing.
Specific over abstract always (psig, deg F, lb, ft, dates). Reader = peer
practitioner ("carry back to your own site"). De-AI discipline: no
throat-clearing, no balanced-clause polish, no em-dash tics, no
"it's not just X, it's Y" cadence.

## Step 3 — Save for review (ONE canonical doc)
Folder naming (stable-keys applied to Drive): UNPUBLISHED issues use the
incident name — `Before Human Error / Issues / <Incident> - <Title> /`
(e.g. `Tesoro Anacortes - Rotting in Plain Sight`). The `NN - ` number prefix
is added ONLY at publish time, when the number freezes. Never bake a mutable
issue number into a folder name. If an issue is renumbered, the renumber is
not complete until any affected folder is renamed — flag the rename to Charlie
(agent cannot rename Drive items) and track it as an open action until done.

Save into the issue folder:
- `Issue - <Title>` (ONE Google Doc) holding: Positioning Pass (internal) +
  the full LinkedIn post + the first-comment text + the article body + a Sources
  block listing all 2+ citations. One doc only — no scratch duplicates.
- `sources/` — the primary report PDF staged, or a source-links note giving the
  CSB Archive `report_path` + live URLs for every citation.
- `figures/` — images (may start empty, but must exist).
The GATE's folder-completeness box covers all three. Then notify Charlie.

## Step 4 — On Charlie's approval, prepare publication (Charlie posts; never auto-post)
- LinkedIn (primary): the FULL teardown as a native text post (NOT a teaser),
  ending with a one-line subscribe CTA; the beehiiv link goes in the FIRST
  COMMENT, not the body (outbound links in the body suppress reach). Keep this
  format until ~1,000 beehiiv subscribers (checkpoint at 500); see operating_guide
  LinkedIn Posting Playbook. Do NOT claim "reach is solved."
- beehiiv (secondary while list is tiny): prepare the post for Charlie to
  schedule (no API; Charlie schedules and publishes).
- Update `issues` (url, status) and `linkedin_posts` (planned row).

### PUBLISH DAY — Charlie's checklist (stage this with every approved issue)
The one expensive miss so far was here, not in drafting (Issue 3: 22k
impressions, first comment never posted, zero email capture). Every publish:
1. Post the full teardown natively on LinkedIn (Tue 9:00 AM ET).
2. IMMEDIATELY post the prepared first comment (beehiiv subscribe link) and
   PIN it. Not optional, not later.
3. Click the pinned link once — verify it resolves to the live subscribe page.
4. Publish the identical article to beehiiv; copy the live `/p/` URL.
5. Update D1: `issues.url` -> live URLs, status='published';
   `linkedin_posts` row gets the post URN/URL; insert a baseline
   `post_snapshots` row (hour ~0).
6. At ~24h: check link engagements > 0 on the post. If 0, the funnel is
   broken — investigate before the next publish.
7. Rename the issue folder to add its now-frozen `NN - ` prefix.

## Step 5 — Buffer + logging
- Keep 2-3 drafted ahead; if buffer <2 after this run, queue the next incident.
- Log to D1 (issues, linkedin_posts, engaged_readers, project_state)
  proactively — do not ask.
- Analytics writes are APPEND-PLUS-UPSERT, never overwrite-only:
  - `linkedin_posts`: upsert by URN — update the existing row, never create a
    duplicate for the same post.
  - `post_snapshots`: INSERT a new row for every analytics capture (post_id,
    urn, hours_since_post, full metrics, source). History is append-only; the
    maturation curve (32h vs 7d) is what the Posting Playbook needs to turn
    hypotheses into rules at 10+ posts. Never delete or overwrite snapshots.

## Companion: Monday report (separate scheduled session)
Every Monday: growth (impressions, followers, subs, CTR), direction, and
money/sponsorship recommendations, using the prior week's matured numbers.
Needs Charlie's weekly LinkedIn analytics export; beehiiv sub counts pulled
directly. Read `operating_guide` (monetization, growth) for context.
- Log per the Step 5 rules: upsert `linkedin_posts` by URN AND insert a
  `post_snapshots` row per post captured. Do not overwrite history.
- Sweep `decision_log` for rows whose `revisit_trigger` has plausibly fired or
  status='revisit'; surface them to Charlie with a recommendation each.
