# Before Human Error — scheduled-session launcher prompts

THE ONLY COPY. These prompts are versioned here, next to SKILL.md, so the
skill and its launchers can never drift apart. Do not keep copies in Google
Drive (the 2026-06/07 Drive copies "Scheduled Session Prompts" v1 + v2 are
superseded by this file — delete them). When the pipeline changes, update
SKILL.md and this file in the same commit.

Paste each block into Claude Code on the web (claude.ai/code) as a recurring
scheduled session. Recommended: FRIDAY 8:00 AM ET (produce draft),
MONDAY 8:00 AM ET (growth/money report). Neither session publishes anything —
publishing is manual and Charlie's alone.

---

## SESSION 1 — FRIDAY: produce the weekly draft

```
Run the weekly Before Human Error production session. Today is Friday.

STEP 0 — LOAD THE SKILL FIRST (every run, do not skip).
This is a PERSONAL skill. It is NOT installed as a slash command and will NOT
auto-load. Fetch and read it yourself before doing anything else:
 - Via the GitHub MCP (get_file_contents), read repo cball8475/skills, branch
   main, file skills/personal/before-human-error/SKILL.md. If that 404s,
   search the repo for before-human-error/SKILL.md and read it.
 - Then read the D1 database "before-human-error"
   (id 06f4ca9c-7089-434b-a34a-b4c4803d23a7): project_state, operating_guide
   (GUARDRAILS first), decision_log, incidents, issues, linkedin_posts.
 - If D1 is unreachable after retries: HALT and report. Never run from memory.
The SKILL.md and D1 are the SOURCE OF TRUTH and may be newer than this prompt.
On any conflict, follow SKILL.md and D1. Execute the skill's full pipeline;
the steps below are only a checklist.

1. Guardrails gate: verify-before-assert; reconcile contradictions (including
   the duplicate-issue-number tripwire); one canonical doc.
2. Buffer check: count issues with status in ('review','scheduled'). If 2-3
   ahead and nothing needs attention, stop and report buffer healthy.
3. Pick next incident: status='backlog', automation='auto-ready', highest
   priority. Confirm the pick by INCIDENT NAME in the run report. Read its
   primary report from incidents.report_path (Drive archive); corroborate with
   WebSearch/WebFetch. 2+ independent sources, no assumptions.
4. Mandatory Positioning Pass, pinned at top of the draft.
5. Draft in the house voice; run the de-AI pass.
6. Save per SKILL.md Step 3: incident-named folder (no number prefix before
   publish), ONE canonical Google Doc + sources/ + figures/. No duplicates.
7. Update D1: issues (status='review', url, subject_line), incidents (status);
   log decisions to decision_log.
8. Do NOT publish or schedule. Notify Charlie: 3-line summary + Drive link.
```

---

## SESSION 2 — MONDAY: growth + money report

```
Run the weekly Before Human Error growth and money report. Today is Monday.

STEP 0 — LOAD THE SKILL FIRST (same as Friday): fetch and read
cball8475/skills @ main : skills/personal/before-human-error/SKILL.md via the
GitHub MCP (it is a personal skill and will NOT auto-load), then read D1
operating_guide (growth, monetization, LinkedIn Posting Playbook),
linkedin_posts, post_snapshots, engaged_readers, issues, decision_log.
If D1 is unreachable after retries: HALT and report. SKILL.md + D1 are the
source of truth and override this prompt on any conflict.

1. Pull last week's matured numbers: beehiiv subs directly; LinkedIn from
   Charlie's weekly export. If the export is not attached, ask Charlie for it
   and pause.
2. Log per SKILL.md Step 5: upsert linkedin_posts by URN (update, never
   duplicate) AND insert a post_snapshots row per post captured. History is
   append-only — never overwrite prior snapshots.
3. Report: growth trend (impressions, followers, subs, CTR); what
   hook/subject/format landed vs the Posting Playbook (as hypotheses with
   sample size, not rules); a direction recommendation; a money/sponsorship
   recommendation — each with its reasoning.
4. Sweep decision_log for revisit_triggers that have plausibly fired; surface
   them with a recommendation each.
5. Log conclusions to operating_guide / decision_log.
6. Recommend, do not act, on anything outward-facing. Deliver the report to
   Charlie.
```

---

## Notes
- Why scheduled sessions, not the in-session cron: scheduled sessions are
  durable; the in-session cron is ephemeral (decision_log #3).
- Publish day is Tuesday 9:00 AM ET; the Friday draft gives the weekend to
  review; Monday uses the prior Tuesday's matured numbers.
- Keep a 2-3 issue buffer (decision_log #2).
- Publish-day execution has its own checklist in SKILL.md Step 4 (born from
  the Issue 3 first-comment miss). It is Charlie's checklist, staged with
  every approved issue.
