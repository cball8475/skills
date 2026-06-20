---
name: csb-investigate
description: Investigate a chemical or industrial incident the way the U.S. Chemical Safety Board (CSB) does — interview for facts, build a timeline, run causal & root-cause analysis, size the effort to the risk, write value-added corrective actions with SMART effectiveness checks, and render a CSB-format report to PDF/DOCX. Use when the user wants to investigate an incident or accident, do a CSB-style or root-cause analysis, write an incident investigation report, or define corrective actions and effectiveness checks.
---

# CSB-Style Incident Investigation

Apply the same tools, analysis, and logic the U.S. Chemical Safety Board uses to
investigate a *new* incident and produce a right-sized, CSB-format report.

This skill is **self-contained** — everything needed is in this folder. The
reference files carry the detail; this file is the orchestration layer. It is
**grounded in the full CSB archive**: see [reference/patterns.md](reference/patterns.md)
for the cross-corpus analysis and [reference/cases/](reference/cases) for ~120
distilled investigations plus ~90 short-form incidents to use as precedents.

## Two rules that override convenience

1. **Question first, assume nothing.** Do the intake interview before any
   analysis. Never invent facts. When a needed fact is missing, present the
   plausible options and ask the user *which assumption to proceed with*, then
   record that choice in the report's **Assumptions & Data Gaps** section.
2. **Match effort to risk.** Size the product to `severity × probability ×
   recurrence`. A simple event with an already-identified root cause gets a short
   note — not a full investigation. Do not over-investigate.

## Workflow (gated — do not skip ahead)

1. **Intake interview** — Walk [intake.md](intake.md). Collect the facts, list
   what is known vs. unknown, and for each material gap offer 2–3 candidate
   assumptions for the user to pick. Only proceed when intake is sufficient.
2. **Triage / right-size** — Use [triage.md](triage.md) to score the risk and
   pick the product tier and depth (incident note → digest/case study → full
   Investigation Report → Hazard Investigation).
3. **Analyze** — To the chosen depth, follow [methodology.md](methodology.md):
   timeline → causal factors → root causes → PSM / safeguard / hierarchy-of-
   controls / regulatory-gap lenses → findings → recommendations. Lighter tiers
   run a subset of the lenses. Pressure-test against
   [reference/patterns.md](reference/patterns.md) and cite precedents from
   [reference/cases/](reference/cases). Push past "operator error" to the
   management-system root cause.
4. **Corrective actions & effectiveness checks** — Follow
   [effectiveness-checks.md](effectiveness-checks.md): screen recommendations
   down to **value-added** corrective actions, then write a **SMART effectiveness
   check** for each, to be run *after implementation*, with owner, pass/fail
   criteria, and a schedule (interval and/or trigger).
5. **Draft** — Fill the matching template in [templates/](templates), per
   [report-structure.md](report-structure.md). Always include the **Assumptions &
   Data Gaps** and **Corrective Actions & Effectiveness Verification** sections.
6. **Render** — Convert the markdown draft to DOCX/PDF:
   `python3 scripts/render_report.py <draft.md> [--out <dir>] [--pdf]`
7. **Persist (optional)** — Only if a Cloudflare D1 database already exists, save
   structured records (see "Optional D1 persistence" below).

## Choosing the template

| Risk band / cause clarity | Product | Template |
|---|---|---|
| Low risk, root cause already clear | Incident note / safety bulletin | [templates/incident-note.md](templates/incident-note.md) |
| Moderate risk, some analysis needed | Investigation digest / case study | [templates/investigation-digest.md](templates/investigation-digest.md) |
| High risk, systemic or unclear cause | Full Investigation Report | [templates/investigation-report.md](templates/investigation-report.md) |
| Broad recurring hazard across sites/industry | Hazard Investigation | full report template, scoped to the hazard |

## Rendering dependencies

`scripts/render_report.py` is defensive and uses whatever is installed:

- **Best:** `pandoc` (DOCX and, with a LaTeX engine, PDF).
- **DOCX fallback:** `python-docx` (`pip install python-docx`).
- **PDF fallback:** `libreoffice --headless` converts the DOCX to PDF.

The script prints exactly which artifacts it produced and where. If only DOCX can
be produced, that is fine — DOCX satisfies the requested output.

## Optional D1 persistence

Skip unless a database already exists. The schema is in
[d1-schema.sql](d1-schema.sql) (SQLite-compatible).

1. List databases via the Cloudflare MCP `d1_databases_list`. If none exists,
   stop — do **not** create one unless the user explicitly asks.
2. If the target DB lacks the tables, apply `d1-schema.sql` with
   `d1_database_query`.
3. Insert the incident plus its timeline, causal factors, root causes, findings,
   recommendations, corrective actions, and effectiveness checks. Effectiveness
   checks store a `scheduled_run_date` / trigger so they can be tracked and run
   after the corrective action is implemented.
