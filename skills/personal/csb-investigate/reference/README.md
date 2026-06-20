# CSB Reference Library

A grounded knowledge base distilled from the user's full CSB Archive (the
"Before Human Error" source corpus). It makes this skill reason from real cases,
not just generic theory, and doubles as a teardown source library.

## What is here

- **[patterns.md](patterns.md)** - the analytical synthesis across the whole
  archive: recurring root-cause archetypes, the PSM elements that fail most, a
  hazard taxonomy, recommendation archetypes, and the "beyond human error" method.
  Read this first.
- **[cases/](cases/)** - one structured record per investigation, grouped into
  files by CSB archive id range, plus the short-form summary-volume incidents.

## Coverage

- **123 full investigations and CSB studies/bulletins** distilled from the
  `reports/` archive (every incident folder, ids 3492 to 3641), across
  `cases/cases_*.md` and `cases/cases_backfill_*.md`.
- **94 short-form incidents** from the four CSB "Incident Reports" volumes, in
  `cases/summaries_vol_1-2.md` and `cases/summaries_vol_3-4.md`.

Each full record follows one schema: identity and date, hazard type, materials,
what happened, consequences, sequence, immediate cause, contributing factors,
root causes, failed/missing safeguards, key findings, recommendations by
recipient, PSM elements implicated, the "easy story" vs the "systemic reframe,"
and 2 to 3 transferable Monday-morning checks. Records were extracted directly
from the final CSB investigation reports (or the investigation update where no
final report exists).

## How the skill uses it

- During an investigation (Step 3 of [../methodology.md](../methodology.md)),
  consult [patterns.md](patterns.md) to pressure-test the analysis: which known
  archetype does this match, what safeguard usually fails here, what did similar
  past cases miss.
- To find precedents, grep `cases/` by company, hazard type, equipment, or
  material (for example `grep -ril "hydrofluoric" cases/`).
- For teardown writing, each record already separates the headline "easy story"
  from the systemic reframe and ends with transferable checks.

## Provenance and caveats

Records are AI-distilled summaries of the CSB reports, intended as a fast index
and analytical aid. For quoting, figures, or publication, verify against the
original PDF named in each record's "Source file(s) read" line. Some very large
reports were truncated on read; those records capture the executive summary,
findings, root causes, and recommendations, which sit early in CSB reports.
