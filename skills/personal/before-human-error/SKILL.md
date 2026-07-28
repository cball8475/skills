---
name: before-human-error
description: >-
  Autonomously produces the weekly "Before Human Error" incident-teardown
  newsletter end to end, for Charlie to review and approve. Triggered when
  Charlie says "write article #N": picks that incident, runs the mandatory
  Positioning Pass, drafts a multi-source fact-checked teardown in the house
  voice, runs the de-AI pass, saves ONE canonical doc to Google Drive for
  review, and stages the LinkedIn (full post) + optional beehiiv publication.
  Publishing is manual; Charlie supervises and posts. Maintains a 2-3 issue
  buffer.
---

# Before Human Error — weekly teardown pipeline

## Operating rules (read D1 first)
- DB: `before-human-error` (D1 id `06f4ca9c-7089-434b-a34a-b4c4803d23a7`).
- Before anything, read `project_state` (operating_model_v2, cadence,
  source_policy) and `operating_guide` (GUARDRAILS first, then Decision
  Principle, voice, Positioning Pass, Sourcing & Fact Discipline, LinkedIn
  Posting Playbook, latest market scan). D1 is the source of truth and may be
  newer than this file.
- TRIGGER: when Charlie says "write article #N", run this whole pipeline for
  article N. Publishing is MANUAL — Charlie posts; this skill only drafts +
  stages. Never publish or schedule anything yourself.
- Cadence: WEEKLY, publish Tuesday. LinkedIn is the primary channel; beehiiv is
  secondary while the list is tiny. Keep a 2-3 issue buffer.
- Charlie = approve, review & publish. Always explain the reasoning behind any
  recommendation.

## Step 0 — GUARDRAILS GATE (non-negotiable; full text in operating_guide "GUARDRAILS")
Purpose: stop the recurring failure of stating stale/assumed info as current
fact and letting one data point become a rule. Apply on every run:
1. VERIFY BEFORE ASSERT — re-check every changeable fact (issue/incident status,
   who replied, subscriber/analytics numbers, dates, what is published) against
   its LIVE source this run; never state it from memory. Label anything you
   cannot verify as "per memory, unverified."
2. RECONCILE CONTRADICTIONS — if two records disagree, stop and resolve before
   reporting; never report the convenient one.
3. ONE DATA POINT IS NOT A RULE — conclusions stay hypotheses with their
   evidence and sample size; re-derive from current numbers each run.
4. STABLE KEYS — reference incidents and sponsors by name or hazard type, never
   by issue number.
5. ONE SOURCE OF TRUTH — D1 is canonical (read first); ONE Google Doc per issue;
   `main` is the only repo truth. No duplicates that can drift.

Before handing Charlie ANYTHING to publish, or any status report, the GATE
(all must be YES): [ ] claims 2-sourced or labeled unverified · [ ] statuses
and numbers re-checked against the live source THIS run · [ ] assumptions /
`[NEEDS INPUT]` flagged to Charlie · [ ] one canonical doc, no scratch
duplicates. If any is NO, fix it or flag it before shipping.

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

## Step 0.5 — INCIDENT SELECTION SCREEN (run before drafting; D1 `project_state.incident_selection_screen`)
Do not assume the queued incident is still the right one. Grade the slotted
incident against this screen AND the 10-item gate first; a slot that fails
either is RE-PICKED, not rewritten. Derived from the n=4 breakout analysis
(Issues 3 and 6 broke out; 4 and 5 did not).
1. ORDINARY SANCTIONED TASK — was the victim doing something the reader has
   personally done or authorized?
2. LIVE BLAME STORY — is the operator-blame version still believed, or already
   publicly demolished (BP Texas City, Macondo, Piper Alpha: no gap left)?
3. UNDERSATURATED in LinkedIn EHS content.
4. ICP MATCH — US, ideally Gulf Coast / Texas / Permian, chemical or O&G.
5. PORTABLE MECHANISM the reader may be carrying right now.
6. RCA-TOOL VARIETY vs the last two issues.
7. 2+ independent sources, primary reachable.
Hold as HYPOTHESIS, not law (n=4, with confounders on the record). Re-derive at
10+ posts. Also reconcile the `issues`/`incidents` status pair for the slot
before drafting; they drift.

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

## Step 2.5 — GATE before status->review (mechanical first, judgement second)
Grade in this order. A, B and C are RUN, not asserted. Do not mark any item
YES from impression: Issue 7 shipped with "de-AI pass: YES" self-graded and
had ZERO contractions in 3,045 words.

**A. VOICE CHECK — mechanical, must pass.**
```
python3 voice-check/voice_check.py <body.txt>
```
Exits non-zero on failure. Thresholds: contractions >=6 per 1k words,
triple-fragments <=1, paragraph-punch rate <=55%, connector phrases = 0,
sentence-length stdev >=8. Fix the copy; never relax a threshold. Run it on
the ARTICLE BODY ALONE (strip positioning pass and metadata) and again on the
LinkedIn feed share. Issue 7 baseline for comparison: 0.0 contractions/1k
(FAIL), 2 connectors (FAIL), 1 triple (pass), 14.3% punch rate (pass), stdev
10.4 (pass) — the real defect was narrower than it felt, which is the point of
measuring instead of eyeballing.

**B. FIGURES BEFORE PROSE.** Pull every figure out of the report and LOOK at
it before writing the paragraph that describes it. Issue 7's AcciMap section
described five Rasmussen levels when the CSB diagram has four bands; it was
caught only when the image was finally placed beside the text. No sentence
describing a figure gets written with the figure unopened.

**C. SOURCE-TRACE EVERY SPECIFIC.** For each concrete claim — numbers, quotes,
"the CSB found X" — grep the primary source and point at the line. A detail
that reads well and cannot be traced is a fabrication. Issue 7 Rev2 invented a
beacon that "lit up perfectly" on a CSB test signal; it appears nowhere in the
report and nearly shipped.

**D. The 11-item Carry-Forward gate** (D1 `operating_guide`, "Carry-Forward
Lessons Checklist"). The de-AI item and item 11 are now covered by A; the rest
still need judgement.

## Step 3 — Save for review (ONE canonical doc)
Save to `Before Human Error / Issues / NN - Title /`:
- `Issue NN - <Title>` (ONE Google Doc) holding: Positioning Pass (internal) +
  the full LinkedIn post + the first-comment text + the article body + a Sources
  block listing all 2+ citations. One doc only — no scratch duplicates.
- `sources/` (primary report + corroborating sources), `figures/` (images).
Then notify Charlie for review.

## Step 4 — On Charlie's approval, prepare publication (Charlie posts; never auto-post)
- LinkedIn (primary): the FULL teardown as a native text post (NOT a teaser),
  ending with a one-line subscribe CTA; the beehiiv link goes in the FIRST
  COMMENT, not the body (outbound links in the body suppress reach). Keep this
  format until ~1,000 beehiiv subscribers (checkpoint at 500); see operating_guide
  LinkedIn Posting Playbook. Do NOT claim "reach is solved."
- beehiiv (secondary while list is tiny): prepare the post for Charlie to
  schedule (no API; Charlie schedules and publishes).
- Update `issues` (url, status) and `linkedin_posts` (planned row).

## Step 5 — Buffer + logging
- Keep 2-3 drafted ahead; if buffer <2 after this run, queue the next incident.
- Log to D1 (issues, linkedin_posts, engaged_readers, project_state)
  proactively — do not ask.

## Companion: Monday report (separate scheduled session)
Every Monday: growth (impressions, followers, subs, CTR), direction, and
money/sponsorship recommendations, using the prior week's matured numbers.
Needs Charlie's weekly LinkedIn analytics export; beehiiv sub counts pulled
directly. Read `operating_guide` (monetization, growth) for context.
