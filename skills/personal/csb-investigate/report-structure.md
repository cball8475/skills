# CSB Report Structure

Anatomy of a CSB-format report. The full Investigation Report uses every section;
lighter products use the subset noted under each tier in [triage.md](triage.md).
Modeled on real CSB Investigation Reports (e.g., ExxonMobil Torrance Refinery ESP
Explosion, No. 2015-02-I-CA).

## Front matter
- **Title** — facility, event type, location.
- **Incident date**, **report number**, **publication date**.
- **Product tier** and **risk band** (from triage).
- **Key Issues** — 3–6 bullets naming the central themes (e.g., "Lack of safe
  operating limits," "Operating equipment beyond safe operating life").
- Standard CSB framing note: the CSB is an independent, scientific, non-regulatory
  body that determines causes and issues recommendations; findings are not for
  assigning fault.

## 1. Executive Summary
What happened, the consequences, the key causes, and the headline
recommendations — in plain language, readable on its own.

## 2. Facility / Company Background
The operator, site, ownership history (flag recent acquisitions), and the unit
involved.

## 3. Process Description
The process/operation and equipment, in enough technical detail to understand the
failure — what it does, how it normally runs, and the relevant safeguards.

## 4. Incident Description & Timeline
The sequence of events across the four phases (pre-incident → incident →
emergency response → consequences). Include a consequences subsection (injuries,
damage, environmental/community impact).

## 5. Causal Analysis
The layered analysis: immediate cause → causal/contributing factors → root
causes, supported by the PSM, safeguard, hierarchy-of-controls, and
regulatory-gap lenses (per [methodology.md](methodology.md)).

## 6. Key Issues / Findings
The significant, evidence-based facts the analysis established. Each root cause
should appear here.

## 7. Root Causes
The underlying management-system deficiencies, stated explicitly.

## 8. Safety Recommendations
Numbered, each addressed to a named recipient and tied to a finding/root cause.

## 9. Corrective Actions & Effectiveness Verification
For each value-added corrective action (per
[effectiveness-checks.md](effectiveness-checks.md)), a row/entry with:

| Field | Content |
|---|---|
| Corrective action | What will be done |
| Addresses | Finding / root cause |
| Control tier | Hierarchy-of-controls level |
| Owner | Responsible party |
| Target implementation | Date |
| SMART effectiveness check | What is verified + pass/fail criteria + method |
| Scheduled check date / trigger | When the check runs *after* implementation |
| Status | scheduled / passed / failed / re-opened |

## 10. Assumptions & Data Gaps
Every fact that was missing and the **user-chosen assumption** used in its place
(tagged `[ASSUMPTION]`), plus open items still needing data. This makes every
assumption-dependent conclusion traceable.

## Appendices (full report only)
Evidence index, photos, P&IDs, regulatory references, interview list.
