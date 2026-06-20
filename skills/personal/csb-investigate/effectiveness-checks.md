# Corrective Actions & Effectiveness Checks

After recommendations are written, do two things: keep only the **value-added**
corrective actions, then attach a **SMART effectiveness check** to each — a
verification, run *after the action is implemented*, that the action actually
reduced the risk.

## Step 1 — Screen for value-added corrective actions

A corrective action (CA) is **value-added** only if it durably reduces the risk of
recurrence. Screen every candidate:

**Keep / strengthen when it:**
- Sits high on the hierarchy of controls (eliminate, substitute, engineer out).
- Addresses a **root cause**, not just the immediate cause.
- Is sustainable without constant vigilance (designed-in, not reminder-based).
- Is verifiable — you can later prove it works.

**Drop, downgrade, or rework when it:**
- Is paperwork-only or "re-train / remind staff" with no system change.
- Treats a symptom while the root cause remains.
- Depends entirely on perfect human performance for a high-severity hazard.
- Duplicates an existing control that already failed.

For each kept CA record: the action, the finding/root cause it answers, its
hierarchy-of-controls tier, an owner, and a target implementation date. Note any
candidate you dropped and why — that reasoning is itself useful.

## Step 2 — Write a SMART effectiveness check per CA

The effectiveness check confirms the implemented CA is working. Make it SMART:

- **Specific** — exactly what will be verified and how (audit, measurement,
  observation, records/data review, test).
- **Measurable** — explicit **pass/fail criteria** (a threshold, count, or
  observable state), not "looks good."
- **Achievable** — uses data/access that will realistically exist.
- **Relevant** — measures the *risk reduction*, not just that the task was done.
  Prefer a leading/outcome indicator over "CA was completed."
- **Time-bound** — has a defined run date or window.

Weak vs. strong:
- Weak: "Confirm operators were trained on the new procedure."
- Strong: "90 days after rollout, review 100% of relief-valve work permits for the
  quarter; ≥95% correctly apply the new safe-operating-limit step, with zero
  reseating events on a live unit. Fail → re-open the CA and escalate."

## Step 3 — Schedule the check (after implementation)

Every effectiveness check needs a **when**:

- **Interval after implementation** — a defined lag so there is real operating
  data to judge against. Typical: **30 days** (administrative/procedural changes),
  **60–90 days** (training/behavioral changes needing several cycles), **one full
  operating/turnaround cycle** (engineering changes proven only under real
  operating conditions).
- **And/or a trigger** — e.g., "at the next instance of this maintenance task" or
  "at the next PHA revalidation."
- **Owner** — who runs the check.
- **Re-check rule** — if it fails, re-open the CA, fix, and re-run the check after
  a stated interval. A CA is not closed until its effectiveness check passes.

## Output

These feed the **Corrective Actions & Effectiveness Verification** section of the
report and the D1 `corrective_actions` + `effectiveness_checks` tables. Record per
check: method, pass/fail criteria, `scheduled_run_date` and/or trigger, owner, and
status (`scheduled` → `passed` / `failed` → `re-opened`).
