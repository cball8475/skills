# Triage & Right-Sizing

Match the investigation effort to the incident. Score the risk, factor in how
clear the cause already is, then pick the product tier. **Do not over-investigate
a simple, already-explained event.**

## Step 1 — Score the three factors (1–5 each)

### Severity (actual + worst credible)
| Score | Guide |
|---|---|
| 1 | First aid only; negligible damage/release |
| 2 | Recordable injury; minor on-site damage |
| 3 | Lost-time injury; notable damage or contained release |
| 4 | Serious injury / hospitalization; major damage or reportable release |
| 5 | Fatality(ies); off-site impact; catastrophic loss |

Use the **worst credible** outcome too: a near-miss that could plausibly have
killed someone scores high on severity even if no one was hurt.

### Probability / likelihood of recurrence of the *initiating conditions*
| Score | Guide |
|---|---|
| 1 | Requires a rare, hard-to-repeat combination |
| 2 | Unlikely under current conditions |
| 3 | Could happen again occasionally |
| 4 | Likely without intervention |
| 5 | Conditions still present; expected to recur |

### Recurrence / breadth (systemic reach)
| Score | Guide |
|---|---|
| 1 | One-off, isolated to a single piece of equipment |
| 2 | Could affect a few similar items locally |
| 3 | Unit-wide pattern |
| 4 | Site-wide or repeated history at the site |
| 5 | Industry-wide / common-mode hazard across facilities |

## Step 2 — Risk band

`risk = severity × probability × recurrence` (range 1–125).

| Risk | Band |
|---|---|
| 1–11 | **Low** |
| 12–44 | **Moderate** |
| 45–80 | **High** |
| 81–125 | **Critical** |

Any **fatality, off-site/community impact, or a severity of 5** is treated as
**High or above** regardless of the arithmetic.

## Step 3 — Cause clarity

- **Established** — root cause already identified and well-evidenced.
- **Partial** — immediate cause known; underlying/systemic causes unclear.
- **Unclear** — cause not yet determined.

## Step 4 — Pick the product

| Risk band | Cause clarity | Product / depth |
|---|---|---|
| Low | Established | **Incident note / safety bulletin.** Document the event, the known cause, and the fix. Skip the full lens set. |
| Low–Moderate | Partial | **Investigation digest / case study.** Timeline + causal analysis on the open questions only. |
| Moderate–High | Partial/Unclear | **Full Investigation Report.** Run all methodology lenses. |
| High–Critical | Any | **Full Investigation Report**, plus consider a **Hazard Investigation** if the hazard is industry-wide. |

Guardrail: **Low risk + Established cause → short note.** Don't manufacture a
full investigation when the answer is already known and the stakes are low.
Conversely, never shrink a fatality or off-site event below a full report.

Record the chosen `risk_band` and `product_tier` — they are fields in the report
header and in the D1 `incidents` table.
