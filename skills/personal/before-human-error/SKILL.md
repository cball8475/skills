---
name: before-human-error
description: >-
  Autonomously produces the weekly "Before Human Error" incident-teardown
  newsletter end to end, for Charlie to review and approve. Triggered when
  Charlie says "write article #N": picks that incident, runs the mandatory
  Positioning Pass, drafts a multi-source fact-checked teardown in the house
  voice, runs the de-AI pass, saves ONE canonical doc to Google Drive for
  review, and stages the LinkedIn (full post) + beehiiv publication. Charlie
  approves every issue; on his go Claude publishes it to beehiiv via the API,
  while LinkedIn stays in Charlie's hands. Maintains a 2-3 issue buffer.
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
  article N.
- PUBLISHING (changed 2026-08-01, Charlie's call; supersedes "publishing is
  manual"). The EDITORIAL gate is unchanged: Charlie approves the content of a
  specific issue, every time. What changed is who performs the mechanics after
  that approval.
  - **beehiiv: Claude publishes.** Write endpoints are no longer plan-blocked
    (verified 2026-08-01; `POST /posts` returns a 400 validation error, not the
    old 403 SEND_API_NOT_ENTERPRISE_PLAN). Use `BEEHIIV_API_KEY` from the
    environment. Publish or schedule ONLY the issue Charlie has approved, only
    to pub_c14bc86a-5655-4f9d-884b-daf4c2091c34, and verify the live post after.
  - **LinkedIn: still Charlie.** There is no LinkedIn API access in this
    environment, so the Newsletter edition, the feed share and the pinned first
    comment remain his hands. Nothing about this change touches that.
  - Never publish an issue that has not been explicitly approved. "Approved"
    means Charlie said so for that issue, not that the draft passed the gate.
  - Deletion of posts is permitted for verified strays only, and only after
    reading each one — the four cleaned up on 2026-08-01 were three CSS-only
    blanks and a duplicate of published Issue 2. Read before deleting; a beehiiv
    "New post" draft still reports ~900 words because the template CSS counts.
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
7. Standards & recommendation follow-through — if the investigation issued
   recommendations to standards bodies or regulators, look up the CURRENT
   status of each one THIS RUN; never report them as-published. Most reports
   are years old and already recapped everywhere, so the recommendation ledger
   is usually the only part of the story still moving, and it answers the
   reader's real question: did anything change, and does it reach me? (Issue 8:
   API revised Std 599 in Oct 2025 and the CSB closed the recommendation in Jan
   2026, but API expressly declined the subparagraphs covering EXISTING valves,
   while ASME and VMA sat at initial open status — that check produced the
   entire angle.) CSB status summaries: search "CSB recommendation status change
   <report no> <recipient>", then curl the PDF. Statuses are changeable facts
   under GUARDRAILS #1 — record the verification date in the sources block.
   Full detail in operating_guide "Standards & recommendation follow-through".

## Step 2 — Draft (house structure)
Cold Open -> How the Unit Worked -> What Happened -> The Easy Story ->
What Actually Set It Up -> How They Got Past Human Error -> The Gap ->
Monday Morning Checklist -> Landing Line -> Footer + sources.
Vary the closing "you don't need X, you need Y" line so the template doesn't show.

### Voice
First person, plain, declarative. Concede the obvious before reframing.
Specific over abstract always (psig, deg F, lb, ft, dates). Reader = peer
practitioner ("carry back to your own site").

De-AI discipline runs in two layers. Read operating_guide "De-AI pass v3" for
the full reconciliation; the short version:

LAYER 1 — the general detector: the `avoid-ai-writing` skill in
`skills/productivity/avoid-ai-writing` (on `main` as of 2026-08-01). Run its P0
and P1 severity tiers over every draft (word-list violations, template phrases,
chatbot artifacts, vague attributions, hedge-stacked predictions, significance
inflation). It is the catalogue; do not restate it here.

LAYER 2 — the house deltas, which is everything the general detector cannot
know about this newsletter:
1. CONTRACTIONS ARE A BAND: 6-10 per 1,000 words. Not "more is better." All
   seven published issues average 0.7/1k and BOTH breakouts sit in that set
   (0.5 and 3.3), so the near-absence of contractions is the house register,
   not an AI artifact. The band sits deliberately above that baseline so
   nothing reads as mechanically as Issue 7 (which shipped with zero), and far
   below conversational. Correcting hard in the other direction took an Issue 8
   draft to 21.9/1k, 31x the published mean. Measure it, don't eyeball it. When
   expanding contractions, MASK QUOTED SPANS FIRST or a global replace will
   rewrite verbatim source material.
2. The triple-fragment device ("Not behind schedule. Not incomplete. None.")
   ONCE per piece, maximum. `avoid-ai-writing` independently reaches the same
   rule under "manufactured punchlines and staccato drama": three or more
   same-shape fragments in a row reads as a drumroll. Keep the one that earns
   emphasis, fold the rest into ordinary sentences.
3. Do not end every paragraph on a punch — let some land flat.
4. No summarize-then-label ("Here is what the investigation found").
5. Kill connector throat-clearing: "here's the thing", "worth stopping on",
   "the part that matters".
6. Wilder sentence-length variance — a 45-word sentence, then a four-word one.
   Vary PARAGRAPH length the same way. Structure is the strongest detection
   signal there is; fixing vocabulary while leaving metronomic rhythm changes
   nothing.
7. First person must be SPECIFIC to Charlie's own work, never
   generic-practitioner. Related: no emotional flatline ("what struck me was")
   — if a reaction is claimed, the writing around it has to earn it.

THREE DELIBERATE DEVIATIONS from `avoid-ai-writing`, so nobody "fixes" them:
- The Monday Morning Checklist is ALWAYS exactly three checks. That trips the
  skill's "numbered list inflation" rule. It is a fixed franchise format, not
  padding — but each check must be genuinely discrete, never one idea split to
  reach three.
- The closing comment-bait question stays. The skill's "rhetorical question
  openers" rule is about stalling before a point; this is a CTA soliciting
  replies, at the end, and it drives the comments the issues live on.
- "Concede the obvious before reframing" is the house spine and superficially
  resembles the skill's "false concession structure." The skill's real objection
  is to concessions where both halves are vague. So the concession must name the
  specific true thing ("They did.") and then turn.

MEASURE, don't eyeball, the four checkable ones: `python3 check_voice.py
<draft.md> --baseline <a published issue>`. House budgets are derived from what
published issues actually do, not adopted blind: em dashes <=3.0/1,000 words
(the skill says 1.0; published Issue 6 ran 3.24, Issue 8 landed 2.15), the
15-25 word "robotic band" under 45% of sentences, sentence-length stdev >=8.
IGNORE the skill's TTR floor of 0.40 — type-token ratio falls mechanically with
length, and published Issue 6 measures 0.360 at 1,849 words, so it is a false
positive at teardown length.

Dosage and asymmetry, not elimination. The house voice broke out twice and the
spine stays; `avoid-ai-writing` says the same thing under "over-polishing" —
sanding out every irregularity pushes prose back TOWARD the AI profile.

## Step 2.5 — Pre-review gate (operating_guide "Carry-Forward Lessons Checklist")
Grade every draft against the 11-item carry-forward list before setting
status->review. Run the de-AI pass above (both layers) and `check_voice.py`.

Two writer-side structure tests from `avoid-ai-writing`, worth the two minutes:
- RESHUFFLE IMMUNITY: can two body paragraphs swap without breaking the piece?
  If order doesn't matter you wrote a list of points, not an argument that
  builds. The teardown structure should make this impossible by construction —
  if it isn't, a section is floating.
- TREADMILL TEST: per paragraph, name the one fact, claim or turn it adds. If
  there isn't one, cut it. Restating the premise in fresh words is the most
  common way a teardown gets long without getting better.

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
