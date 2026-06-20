# CSB Analysis & Logic

How the CSB reasons from facts to root causes to recommendations. Run the lenses
to the depth set in triage — lighter tiers use a subset, but the order is always
**timeline → causal factors → root causes → findings → recommendations**.

The CSB is a scientific, non-regulatory body: it determines *causes* and issues
*recommendations*. It does not assign fault or penalties. Keep the tone factual
and systems-focused, not blame-focused.

## 1. Build the timeline (sequence of events)

Reconstruct events in four phases:

1. **Pre-incident** — design, prior conditions, warning signs, decisions and
   changes that set the stage (e.g., a reused procedure variance, a deferred
   repair, an unaddressed prior near-miss).
2. **Incident** — the chain from initiating event to the release/fire/explosion.
3. **Emergency response** — detection, alarms, evacuation, how it was terminated.
4. **Consequences** — injuries, damage, off-site/community impact.

Anchor each entry to evidence (logs, alarms, CCTV, interviews, records). Flag any
step that rests on a user-chosen `[ASSUMPTION]`.

## 2. Causal analysis — layer the causes

CSB causal analysis distinguishes layers; push past the obvious to the systemic:

- **Immediate (direct) cause** — the physical event/condition that produced the
  loss (e.g., flammable vapor reached an ignition source).
- **Causal / contributing factors** — the failures and conditions that allowed
  the immediate cause: equipment, procedures, decisions, missing safeguards.
- **Root causes** — the underlying **management-system** deficiencies behind the
  causal factors (e.g., no safe operating limits defined; PHA never evaluated this
  scenario; MOC bypassed; mechanical-integrity program did not catch the
  degradation). Root causes are where recommendations must bite.

Technique: for each causal factor ask "why was this allowed to exist or persist?"
until you reach a management system that could have prevented it. Stop at causes
the organization can actually control.

## 3. Apply the analytical lenses

### Process Safety Management (PSM) element review
Test the incident against the relevant PSM elements and name the gaps:
- Process safety information / P&IDs accuracy
- **Process hazard analysis (PHA)** — was this scenario identified and safeguarded?
- **Operating procedures & safe operating limits** — defined, current, followed?
- **Management of change (MOC)** — was the change/variance reviewed and approved?
- **Mechanical integrity** — inspection/testing of the failed equipment
- Training & competency; contractor management
- Pre-startup safety review; emergency planning & response
- Incident investigation & action tracking; operating discipline / human factors

### Safeguard / barrier effectiveness
List the barriers that should have stopped or mitigated the event. For each:
present? functioned? adequate? Distinguish **prevention** barriers (stop the
event) from **mitigation** barriers (limit consequences). Missing and failed
barriers are prime sources of findings.

### Hierarchy of controls (drives recommendation quality)
Rank possible controls and prefer the strongest:
**Eliminate → Substitute → Engineering controls → Administrative controls → PPE.**
A recommendation that only adds a procedure or training (administrative) is
weaker and less durable than one that removes the hazard or engineers it out.

### Regulatory & industry-standard gap analysis
Identify where regulation or consensus standards were absent, ambiguous, not
followed, or insufficient: OSHA PSM (29 CFR 1910.119), EPA RMP (40 CFR 68), state
PSM programs, and standards such as NFPA, API, ASME, ISA. Note gaps that warrant a
recommendation to a regulator or standards body, not just the company.

## 4. Key findings

State the significant facts the analysis established — concise, evidence-based,
and neutral. Findings are the bridge from analysis to recommendations: every root
cause should surface as one or more findings.

## 5. Safety recommendations

Write recommendations that are:
- **Tied to a finding/root cause** — no orphan recommendations.
- **Addressed to a specific recipient** — the company, a regulator, an industry
  body, or a standards organization.
- **Action-oriented and verifiable** — say what must change, strongly enough that
  an effectiveness check (see [effectiveness-checks.md](effectiveness-checks.md))
  can later confirm it worked.
- **As high on the hierarchy of controls as practical.**

Recommendations then feed the corrective-action and effectiveness-check stage.
