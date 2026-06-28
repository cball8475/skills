---
name: before-human-error
description: >-
  Autonomously produces the weekly "Before Human Error" incident-teardown
  newsletter end to end, for Charlie to review and approve. Intended to fire on
  a schedule every Friday (via a Claude Code scheduled session), so no manual
  invocation is needed. Picks the next incident from the backlog, runs the
  mandatory Positioning Pass, drafts a multi-source fact-checked teardown in the
  house voice, runs the de-AI pass, saves it to Google Drive for review, and
  stages the beehiiv + LinkedIn posts for Tuesday 9 AM ET publication. Maintains
  a 2-3 issue buffer. Charlie supervises only; he does not write or operate.
---

# Before Human Error — weekly teardown pipeline

## Operating rules (read D1 first)
- DB: `before-human-error` (D1 id `06f4ca9c-7089-434b-a34a-b4c4803d23a7`).
- Before anything, read `project_state` (cadence, operating_model,
  source_policy, signature_sections, editorial_angle) and `operating_guide`
  (Decision-Making Principle, voice, Positioning Pass, Sourcing & Fact
  Discipline, latest market scan). D1 is the source of truth and may be newer
  than this file.
- Cadence: WEEKLY. Publish Tuesday 9:00 AM ET. Keep a 2-3 issue buffer.
- Charlie = approve & review ONLY. Never publish without his approval.
- Always explain the reasoning behind any recommendation.

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
`auto-ready` when its primary report is staged in the Drive archive OR on a
network-allowlisted domain (the current environment blocks arbitrary web
fetch). For a `pending-source` incident, stage the primary report in Drive
first, or handle it as a supervised special. Never let the egress limit shrink
the editorial scope — stage the source instead.

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

## Step 3 — Save for review (smart Drive practice)
Save to `Before Human Error / Issues / NN - Title /`:
- `Issue NN - Draft` (Google Doc) with Positioning Pass output at the top and a
  Sources block listing all 2+ citations. One canonical Doc - no duplicates.
- `sources/` (primary report + corroborating sources), `figures/` (images).
Then notify Charlie for review.

## Step 4 — On Charlie's approval, stage publication for Tue 9 AM ET
- beehiiv: create the post, schedule Tue 9:00 AM (email+web).
- LinkedIn: output a ready-to-paste post for Charlie to drop into LinkedIn's
  native scheduler (cannot auto-post to a personal profile).
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
