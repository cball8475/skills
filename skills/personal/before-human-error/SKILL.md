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

## Step 2.5 — CARRY-FORWARD LESSONS GATE (grade every draft before it goes to review)
This is the continuous-improvement loop made executable (operating_guide id 13):
every issue must be graded against what earlier issues taught, so quality
compounds instead of resetting. Do NOT set status -> review until each box is YES
or explicitly flagged to Charlie with a reason. When a new issue teaches a new
lesson (a hook/format/tool that landed or flopped), ADD it here and log it to
operating_guide so the next issue inherits it.

1. DATA-TRAIL SPINE. "What Actually Set It Up" carries the specific evidence the
   investigators actually pulled — recorded process trends (temp/pressure/level),
   as-found hardware, chemistry/metallurgy, audit gaps — not a narrative-only
   causation. Give the reader concrete numbers and artifacts (Issue 3 standard).
2. INVESTIGATIVE-TOOLS PASS. "How They Got Past Human Error" names and WORKS
   ONE to THREE concrete, transferable RCA methods a practitioner already uses,
   so the reader can reuse them — not "the investigators were independent." Use
   as many as the incident actually earns: often ONE well-worked tool beats three
   name-dropped ones, so don't force multiple. Pick from: 5 Whys, Ishikawa /
   fishbone (People, Methods/Procedures, Equipment, Materials, Environment,
   Management), barrier analysis / bowtie, causal tree / AcciMap, TapRooT, MORT,
   or Susca's hazard-gatekeeper lens (operating_guide id 17). Across issues, vary
   which tool leads — don't open with the same single method every time. Whatever
   you pick, show it walking the reader OFF the operator and up to the systemic
   decision. Chains must be LINEAR — each answer becomes the subject of the next
   question; don't skip a link (a lost flow has its own "why did it stop") and
   don't branch into repeated "why not / why not". Validate a 5 Whys by reading it
   BACKWARDS saying "therefore": if each step implies the one below it and it
   still tracks, the chain is sound.
3. AUTHORITATIVE FIGURES. Include 1-3 figures from the investigation's OWN report
   (CSB/RC/NTSB), captioned with a source credit — never custom graphics Charlie
   has to approve (Issue 4 lesson). If the case is non-CSB and has no reusable
   figure, spec the best available image and flag it for sourcing; don't ship
   figureless if a real one exists.
4. CITE & TAG THE CANON (operating_guide id 16). Name/plan to tag the relevant
   canon for THIS incident — Conklin, Dekker, Kerin, Hopkins, CCPS Beacon, plus
   the primary investigation body. On non-US cases tag the regional canon (e.g.
   Longford -> Hopkins + Kerin).
5. FIRST-PERSON PRACTITIONER VOICE. At least two genuine "I / on your own site"
   peer moments; concede the obvious before reframing; run the de-AI pass. Not
   detached third person.
6. LEADING-INDICATOR / NEAR-MISS BEAT. Surface the ignored precursor or near-miss
   as the hook, verified to the 2-source bar. (This is the Positioning Pass beat —
   make sure it survives into the BODY, not just the internal notes.)
7. SIGNATURE ENGAGEMENT DEVICES. Engineer for SAVES + COMMENTS specifically —
   they are the amplified engagement types and signal reference value (Issue 3:
   99 comments, 64 saves); do not chase raw likes. In-body save-the-checklist /
   ten-minute toolbox-talk line (proven Issue 3); a closing comment-bait question
   ending "...I read every one"; Monday Morning Checklist = exactly three
   specific, actionable checks.
8. DISTRIBUTION LOCKS. LinkedIn Newsletter CTA = "Subscribe here on LinkedIn"
   (locked Rev9); beehiiv link in the FIRST COMMENT only (pinned), selling the
   inbox-a-day-early upgrade; LinkedIn body == beehiiv body, identical; 2+
   independent sources cited. Publish as a LinkedIn Article/Newsletter (its
   auto-share is what carries the feed reach), business-morning Mon/Tue ~9am ET.
9. TOPIC-FIT / ON-LANE. The incident is a process-safety teardown with an
   operator-blame-reversal angle — the subject itself self-selects the ICP and is
   the single biggest reach driver (on-topic broke out 2/2; an off-topic post
   died at 314; Issue 3 reached O&G 25% / Chem Mfg 13%, PETRONAS/Shell/bp). Do
   NOT drift off-lane for variety; vary the incident, not the beat.
10. FEED-FIRST HOOK. The headline + first ~2 lines must land the curiosity-gap
    reversal ("blamed the operator / the report didn't") ABOVE the "see more"
    fold — the reframe has to be visible before the reader clicks, not buried
    after the Cold Open's setup.

GATE OUTPUT -> TRACKER. On completing the gate, create/update this issue's row in
`article_tracker`: issue_number, publish_week, working_title, status, and the
change ledger — `added` / `removed` / `improved` vs the prior issue — plus
`gate_notes` for any item not YES. This row IS the continuous-improvement record;
it makes each week's craft change visible and is the source for the Monday report.

## Step 3 — Save for review (ONE canonical doc)
Save to `Before Human Error / Issues / NN - Title /`:
- `Issue NN - <Title>` (ONE Google Doc) holding: Positioning Pass (internal) +
  the full LinkedIn post + the first-comment text + the article body + a Sources
  block listing all 2+ citations. One doc only — no scratch duplicates.
- `sources/` (primary report + corroborating sources), `figures/` (images).
Then notify Charlie for review.

### Drive handling until edit access exists (READ THIS before saving)
The connected Google Drive tool can CREATE, read, copy and search files but has
NO edit-in-place or delete operation. So you cannot revise a Doc after saving it
and you cannot remove old ones. To avoid a v1/v2/v3 trail:
- Write the COMPLETE, finalized content on the FIRST create — run the whole
  Step 2.5 gate BEFORE saving, not after. Treat the first save as final.
- If a revision is unavoidable, create the new doc, repoint `issues.url` to it,
  and hand Charlie the list of superseded file IDs to delete in one pass (he
  deletes; you can't). Never leave the folder with two docs and no pointer to
  which is canonical — `issues.url` is the tiebreaker.
- Upload figures as their own files in the issue folder (svg/png), captioned and
  source-credited; flag any image that still needs licensing.
- When edit access does land (a Drive/Docs MCP exposing files.update or Docs
  batchUpdate), switch to editing the ONE canonical doc in place and drop this
  workaround.

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
- Log to D1 proactively — do not ask: `issues` (url/status/subject),
  `linkedin_posts`, `engaged_readers`, `project_state`, `decision_log` (any
  non-trivial call), and `article_tracker` (this issue's change-ledger row from
  Step 2.5). Track any open pre-publish fix in `action_items`.

## Step 5.5 — Post-publish metrics capture (each time Charlie shares an analytics export)
Reach + engagement mature over ~5-7 days; capture them as they arrive.
- Per reading, append a `post_snapshots` row (impressions, members_reached,
  saves, comments, reposts, article_views, profile_viewers, followers_gained,
  engagement_rate_pct, hours_since_post).
- Update the issue's `article_tracker` row: `first_24h_impressions` (earliest
  breakout signal); the LEADING set (`li_saves`/`li_comments`/`li_reposts`/
  `li_article_views`/`li_profile_viewers`) and the LAGGING set (`lag_impressions`/
  `lag_members_reached`/`lag_followers_gained`/`lag_engagement_rate_pct`/
  `lag_new_subscribers`); plus `follows_per_1k`.
- Judge with the LEADING vs LAGGING framework (operating_guide id 21): call a live
  post on leading indicators within 24h; breakout bar = first-24h impressions
  > ~10x current follower count OR > 25k absolute. Read viral mechanics in id 20.
- VERIFY-BEFORE-ASSERT: a fresh export SUPERSEDES an earlier snapshot — correct
  the stale number, don't stack it. Update `subscribers_status` (beehiiv +
  LinkedIn newsletter) when it changes; flip resolved `action_items` to done.

## Companion — Monday growth report (separate scheduled session; framework in operating_guide id 18)
Drive it off the tables, not memory. Structure (matured prior-week numbers):
(a) THE NUMBERS from `article_tracker` + latest `post_snapshots` +
    `subscribers_status` — followers total/net, subscribers (beehiiv + LinkedIn
    newsletter), and the week's LEADING + LAGGING split.
(b) WHAT MOVED & WHY as hypotheses with sample size (never a rule off one post).
(c) CONVERSION — `follows_per_1k` (and subs/1k) vs the running baseline; one
    lever to test.
(d) BREAKOUT RATE — count posts clearing the bar; note the `first_24h_impressions`
    signal.
(e) AUTHORITY/ally wins; (f) MONEY/sponsorship (from `sponsors`); (g) ONE decision
    for the week + any open `action_items`.
Inputs from Charlie weekly: follower total + beehiiv sub count + the aggregate
export. Measure the COMPOUNDING assets (followers + subs + authority), NOT the
volatile per-post reach.
