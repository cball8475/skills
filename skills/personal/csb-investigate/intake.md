# Intake Interview

Run this **before** any analysis. The goal is to collect facts, not to theorize.
Ask in batches, confirm what you heard, and keep a running **known vs. unknown**
list. Make no assumptions on your own.

## How to handle a missing fact

When a fact is needed for the analysis and the user does not have it:

1. Say plainly that it is missing and why it matters.
2. Offer **2–3 specific candidate assumptions** (not open-ended), each with its
   implication for the analysis.
3. Ask the user which assumption to proceed with — or to mark it as an open item.
4. Record the chosen assumption verbatim in the report's **Assumptions & Data
   Gaps** section, tagged as `[ASSUMPTION]`, so every downstream conclusion that
   depends on it is traceable.

Never silently fill a gap. An explicit, user-chosen assumption is acceptable; a
hidden guess is not.

## What to collect

### 1. Incident basics
- Facility / company / operator and ownership (note recent acquisitions).
- Location (site, unit, specific equipment).
- Date and time; when it was reported and to whom.
- One-line description of what happened.

### 2. Materials & process
- Chemicals/materials involved, quantities, phase, and hazards
  (flammable, toxic, reactive, corrosive, asphyxiant, dust).
- The process or operation in progress (normal ops, startup, shutdown,
  maintenance, turnaround, emergency).
- Equipment and its design intent, age, and condition.

### 3. Consequences (drives the risk score)
- Fatalities and injuries (on-site workers, contractors, public).
- Property damage (estimate) and business interruption.
- Environmental release / off-site impact / community exposure or evacuation.
- Near-miss potential: worst credible outcome had conditions differed.

### 4. Sequence / timeline
- Pre-incident conditions and any warning signs or prior similar events.
- The chain of events leading to the release/explosion/fire.
- Emergency response and how the event was terminated.
- Source data available (DCS/SCADA logs, alarms, CCTV, interviews, photos,
  maintenance records, P&IDs, procedures, permits).

### 5. Existing findings (drives proportionality)
- Has anyone already determined a cause? Immediate cause? Root cause?
- Confidence in that determination and evidence behind it.
- Any internal investigation, regulator finding, or vendor report already done.
- This is the key question for right-sizing: a well-supported, already-identified
  root cause on a low-risk event points to a short note, not a full investigation.

### 6. Management systems & safeguards
- Were there procedures / safe operating limits for the activity?
- Process hazard analysis (PHA) coverage of this scenario.
- Management of change (MOC) for any recent modification or variance.
- Mechanical integrity / inspection history of the failed equipment.
- Safeguards/barriers that were present, and which failed or were absent.

### 7. Regulatory & standards context
- Applicable regimes: OSHA PSM (1910.119), EPA RMP, state PSM, etc.
- Relevant consensus standards: NFPA, API, ASME, OSHA general industry.
- Any prior citations, recommendations, or audit items on point.

## Exit criteria

Proceed to triage only when you can state, in one paragraph each: what happened,
the consequences, the sequence, and what is known vs. assumed. If the event is
clearly minor and the root cause is already established and evidenced, you may
move quickly to triage and a short product.
