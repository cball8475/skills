---
name: before-human-error
description: >-
  Runs the weekly "Before Human Error" incident-teardown newsletter end to
  end — write, revise, publish, verify. Triggered when Charlie says "write
  article #N": picks that incident, runs the mandatory Positioning Pass,
  drafts a multi-source fact-checked teardown in the house voice, runs the
  de-AI pass, saves ONE canonical doc to Google Drive for review, and stages
  the LinkedIn (full post) + beehiiv publication (identical body, Before
  Human Error account only). Charlie posts manually; the skill then runs
  post-publish verification (right account, latest text, right thumbnail)
  and syncs every revision to D1 so edits carry forward instead of stale
  drafts resurfacing. Maintains a 2-3 issue buffer.
---

# Before Human Error — weekly teardown pipeline

## Operating rules (read D1 first)
- DB: `before-human-error` (D1 id `06f4ca9c-7089-434b-a34a-b4c4803d23a7`).
- Drive root (canonical): `Before Human Error` folder
  https://drive.google.com/drive/folders/1aN91lBexaDwfHjc0uWZYW6nuG2NqvY3V
  (`Issues/` scaffold = `1hLu4QEOzjOgFs5O05msazgP9SFR_vqKr`; details in
  `project_state.drive_canonical_folder`).
- beehiiv: TWO accounts exist. Newsletter posts go ONLY to **Before Human
  Error** (`pub_c14bc86a-5655-4f9d-884b-daf4c2091c34`,
  before-human-error.beehiiv.com). "Charlie's Newsletter" (`pub_e0e27b7b…`,
  charlies-newsletter-d1622b.beehiiv.com) is legacy — never post there.
  Env `BEEHIIV_*` vars have pointed at the wrong account before: verify
  `GET /v2/publications` names "Before Human Error" before trusting any key.
  The write API (create/update post, thumbnail) is enterprise-gated (403
  `SEND_API_NOT_ENTERPRISE_PLAN`) — every beehiiv publish/edit/thumbnail is
  MANUAL by Charlie; the session stages exact inputs and verifies the live
  result. See `project_state.beehiiv_accounts`.
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

## Step 3 — Save for review (ONE canonical doc)
Save to `Before Human Error / Issues / NN - Title /`:
- `Issue NN - <Title>` (ONE Google Doc) holding: Positioning Pass (internal) +
  the full LinkedIn post + the first-comment text + the article body + a Sources
  block listing all 2+ citations. One doc only — no scratch duplicates.
- `sources/` (primary report + corroborating sources), `figures/` (images —
  the cover banner lives here; full designed banner WITH text is correct and
  fits beehiiv/LinkedIn thumbnails as-is, verified Issues 1-3).
Then notify Charlie for review.

## Step 3.5 — Revision protocol (edits carry forward — non-negotiable)
The 2026-07-02 Issue-3 failure: a FINAL doc superseded the draft, D1 was never
re-synced, and a later session pasted the stale D1 text to the wrong beehiiv
account. These rules prevent the repeat:
1. ONE canonical doc per issue holds the LATEST approved text at all times.
   If a revision produces a new doc (e.g. "Issue NN - FINAL ARTICLE"), that doc
   becomes canonical; retitle the old one "(superseded)" or fold it in — never
   leave two docs that both look current.
2. SAME-SESSION SYNC: any edit to the canonical doc after approval is mirrored
   into `issues.notes` (full text + dated `[SYNC]` line) before the session
   ends. `issues.notes` MIRRORS the canonical doc; the doc wins for body text,
   D1 wins for status/metadata. On any conflict, stop and reconcile (GUARDRAIL 2).
3. NEVER serve paste-ready body text from D1 or memory. Re-read the canonical
   doc live, confirm it is the newest doc in the issue folder (by title and
   modifiedTime), then deliver.
4. If a published channel already carries older text, flag it, stage the
   correction pack for Charlie, and record the discrepancy in `issues.notes`
   until the live page verifies clean.

## Step 4 — On Charlie's approval, stage publication (Charlie posts; never auto-post)
Deliver ONE publish pack per issue, built ONLY from the canonical doc (Step 3.5
rule 3). It contains, per channel:
- LinkedIn (primary): the FULL teardown as a native text post (NOT a teaser),
  ending with a one-line subscribe CTA; the beehiiv link goes in the FIRST
  COMMENT, not the body (outbound links in the body suppress reach) — POST AND
  PIN the comment. Cover image = `Issues/NN/figures` banner. Keep this format
  until ~1,000 beehiiv subscribers (checkpoint at 500); see operating_guide
  LinkedIn Posting Playbook. Do NOT claim "reach is solved."
- beehiiv (identical body, per operating_model_v2): paste into a NEW post on
  **Before Human Error** — Charlie confirms the editor URL/domain is NOT
  charlies-newsletter before publishing. Set subject line + preview text from
  the canonical doc header, upload the same `figures/` cover banner as the
  thumbnail, publish web+email (or web-only for backfills), then send the
  live `/p/` URL back for logging.
- Pre-log D1: `linkedin_posts` planned row (ALWAYS set `issue_id`), `issues`
  status.

## Step 4.5 — Post-publish verification (mandatory; publish is NOT done until this passes)
Run in the same session the URLs arrive, or the next session:
1. Fetch the live beehiiv page. Verify (a) domain is
   before-human-error.beehiiv.com, (b) body matches the canonical doc — check
   3+ distinctive phrases that exist ONLY in the latest version, (c) the post
   appears on /archive.
2. Download the live thumbnail and byte/dimension-compare against the issue's
   `figures/` cover (Issue-3 reference: LinkedIn cover == Drive cover, md5
   `4117fac0…`). Mismatched or wrong-issue banner = stage a manual swap for
   Charlie (API can't do it). If banners LOOK cropped on Home/Archive, the
   cause is the site builder's post-card setting (cards rendered 1:1
   `object-fit:cover` as of 2026-07-02) — fix the card image-fit/aspect in
   the builder; NEVER re-crop or pad the banner files to compensate.
3. Same idea for LinkedIn: confirm the post is live, first comment posted and
   pinned with the right link, cover renders.
4. Only then flip D1: `issues.status='published'` + `issues.url`,
   `project_state.beehiiv_issueN_url`, `linkedin_posts` row (urn, post_url,
   `issue_id`), and any funnel_status update.
5. Any failure: record it in `issues.notes` + funnel_status, deliver the fix
   pack to Charlie, and keep the issue flagged until a re-verify passes.

## Step 5 — Buffer + logging
- Keep 2-3 drafted ahead; if buffer <2 after this run, queue the next incident.
- Log to D1 (issues, linkedin_posts, engaged_readers, project_state)
  proactively — do not ask. `linkedin_posts.issue_id` is required on every
  issue post row (rows without it break the issue↔analytics join).

## Companion: Monday report (separate scheduled session)
Every Monday: growth (impressions, followers, subs, CTR), direction, and
money/sponsorship recommendations, using the prior week's matured numbers.
Needs Charlie's weekly LinkedIn analytics export; beehiiv sub counts pulled
directly. Read `operating_guide` (monetization, growth) for context.
