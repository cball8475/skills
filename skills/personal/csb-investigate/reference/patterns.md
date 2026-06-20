# CSB Patterns: What 120+ Investigations Teach

Synthesis across the full CSB archive in [cases/](cases/). This is the analytical
core of the skill: the recurring root causes, the safeguards that fail, and the
checks that catch them. Use it two ways: as a lens while investigating a new
incident (Step 3 of [methodology.md](../methodology.md)), and as the source of
the transferable "what to check at your own plant" lessons.

Plain language, no em dashes (project house style).

## The method behind the findings: beyond human error

The single most repeated lesson in the archive is that "operator error" is a
description of the trigger, not an explanation of the accident. In nearly every
fatal case the operator was the last person in a long line of decisions made by
designers, managers, and prior investigators. The CSB gets past the easy story
with a method worth copying:

1. **Independence.** The investigator has no stake in stopping at the operator.
   Keep asking "why was that allowed to exist or persist" until you reach a
   management system the organization controls.
2. **Layered causation.** Separate the immediate cause from the contributing
   factors from the underlying root causes. Recommendations must bite at the root
   (management-system) layer, not the trigger.
3. **The cause lives before the human.** If a single human slip can cause a
   release, fire, or fatality with no engineered backstop, the problem is the
   missing backstop, not the slip. Ask of every serious hazard: "what happens
   when, not if, someone makes the expected mistake?"
4. **Recommendations to everyone who could have prevented it.** Company, corporate
   parent, regulator, standards body, and industry. The fix is rarely just "retrain."

## The recurring root-cause archetypes

These appeared again and again across decades, industries, and hazard types.

### 1. The hazard was never identified, so no barriers were ever built
The deadliest single pattern. The process owner did not recognize the hazard
(reactive/runaway chemistry, combustible dust, an asphyxiant, a thermal
decomposition), so there was no PHA of it, no safeguards, no procedures, no
training. Absence of a PHA for a hazard is itself a leading indicator of
catastrophe.
- Examples: Givaudan (sugar runaway), T2 Labs (runaway), Bayer CropScience,
  Morton, Synthron, Imperial Sugar and West Pharmaceutical (concealed dust),
  Didion (corn dust), Hoeganaes and AL Solutions (metal dust), MGPI and Midland
  (incompatible mixing).
- Check: pull your "low hazard / non-reactive / inert / just dust" list and ask
  whether anyone actually tested or analyzed each at operating and credible upset
  conditions, or just assumed.

### 2. Failure to learn (prior near-misses and other sites ignored)
Almost every catastrophe had precursors: prior small fires, prior releases, a
near-identical event at a sister plant, an unimplemented prior recommendation.
The incident-investigation and recommendation-tracking systems closed events
without fixing the underlying hazard.
- Examples: Formosa Illiopolis (near-identical Baton Rouge event one year earlier,
  filed as "not us"; its own 60-day-prior near miss with an overdue corrective
  action), BP Texas City, Bhopal-style repeat releases, Isotec (three prior
  detonations), Bethlehem Steel (three January warnings before the fatality).
- Check: take your last three near misses and ask "did we decide it did not apply
  to us because our setup was a little different." Then check whether any
  corrective action is past its due date on a serious hazard.

### 3. Management of change failed at the transition
The hazard entered through a change that was never formally reviewed: scale-up,
decommissioning leaving a dead-leg, a temporary hose, a reused procedure variance,
a new feedstock, a relocated/aged asset returned to service, winterization
insulation that trapped corrosion.
- Examples: Morton (1,000 to 2,000 gal scale-up), Bethlehem Steel and Suncor
  (dead-legs), Valero and PBF (temporary hoses), ExxonMobil Torrance (reused 2012
  variance), Givaudan (1978 reactor relocated and restarted), ArcelorMittal
  (improper repair patches).
- Check: every temporary fix, every "we have always done it this way" workaround,
  and every change that crosses a threshold nobody re-evaluated.

### 4. Maintenance, turnaround, and non-routine work is the highest-risk window
A large majority of the fatal incidents happened during startup, shutdown,
maintenance, cleaning, repair, or turnaround handoff, not normal production.
Controls for non-routine work (vessel closure, line breaking, permits, hazard
re-briefing) were consistently weaker than for steady-state operation.
- Examples: Dow Louisiana (work lights left in an EO drum at turnaround), PEMEX
  Deer Park (wrong flange opened), Tosco Avon (live repair on a crude tower),
  ExxonMobil Baton Rouge (valve disassembly under pressure), most hot-work deaths.
- Check: does non-routine and turnaround work get a real pre-task hazard review,
  or only a steady-state PHA that never imagined the maintenance state?

### 5. Isolation and energy control verified on paper, not in reality
Workers confirmed a lock or tag was present but did not verify the valve was
actually in the safe position or that the line was truly depressurized and drained.
- Examples: AdvanSix, Sasol, Olin, PBF Martinez, Tyson, DuPont, Valero Delaware
  City (nitrogen), many line-break injuries.
- Check: does your isolation procedure require a positive zero-energy / zero-
  pressure verification step, not just "lock applied"?

### 6. Human action credited as a safeguard with no engineered backstop
PHAs and LOPA studies routinely listed "operator will notice and act" as a layer
of protection. Under real incident conditions operators lacked the procedure,
the information, the instrument, or the time. The barrier that was supposed to
matter was a person being perfect.
- Examples: Formosa Illiopolis (verbal-permission bypass), BP-Husky Toledo,
  Marathon Martinez, Honeywell Geismar, PEMEX Deer Park.
- Check: for your worst-case releases, trace what actually prevents them. If the
  honest answer is a person following a procedure with no engineering backstop,
  that is a Formosa gap.

### 7. The safeguard failed exactly when it was needed
Relief systems sized for the wrong scenario, detection installed but nonfunctional,
alarms silenced or flooded, mitigation systems disabled by the very event they
were meant to handle.
- Examples: Givaudan (relief roughly 4x too small for decomposition), Pryor Trust
  (critical alarm silenced), Philadelphia Energy Solutions (water spray knocked
  out by the blast), Aghorn (H2S detection nonfunctional), BP-Husky (12-hour alarm
  flood masked the signal), Arkema (refrigeration lost with power).
- Check: what scenario was each relief device and safety instrumented function
  actually sized and located for, and does it survive the event it must mitigate?

### 8. Mechanical integrity: finding a defect is not fixing it; inspecting for the
wrong damage mechanism
Corrosion, thinning, creep, and fatigue that programs either missed (wrong damage
mechanism, wrong location, frequency too low) or documented but never repaired.
- Examples: Tesoro Anacortes and PES (high-temperature hydrogen attack and HF
  corrosion), ExxonMobil (sulfidation), ONEOK (bottom-of-pipe corrosion), Marathon
  Texas City (known coupling defect unrepaired), D.D. Williamson and Loy-Lange
  (uninspected, uncertified pressure vessels).
- Check: is the actual damage mechanism for each circuit in the inspection
  program, and is every open inspection finding tracked to repair with a deadline?

### 9. Facility siting and occupied buildings put people in the blast or cloud
Control rooms, trailers, and break rooms inside the consequence zone; reactive
processes sited next to offices, daycares, or the public.
- Examples: Givaudan (control room ~40 ft away, not blast-resistant), BP Texas
  City (trailers), Concept Sciences (industrial park with a daycare), Loy-Lange
  (vessel ejected off-site, killed members of the public).
- Check: who sits, works, or lives inside the worst credible consequence radius,
  and is occupied space hardened or moved?

### 10. Regulatory coverage gaps leave high-hazard operations unguarded
Many incidents involved facilities or hazards outside OSHA PSM or EPA RMP because
of specific exemptions: reactive chemicals not on the lists, atmospheric storage,
oil and gas production/workover, retail, or sub-threshold quantities. Small
operators frequently did not even know whether PSM applied.
- Examples: the 2002 Reactive Hazard Study (more than half of 167 reactive
  incidents involved chemicals outside PSM/RMP), Sonat, Aghorn, ITC, AB Specialty,
  Wendland and Optima Belle (oil and gas).
- Check: do not assume "not covered" means "not hazardous." Apply PSM-grade rigor
  to any process that can kill, regardless of the regulatory floor.

## PSM elements that fail most often

In rough order of how often they were decisive in the archive:
1. Process hazard analysis (hazard not identified, or scenario not analyzed)
2. Management of change (especially temporary, scale-up, decommissioning, turnaround)
3. Mechanical integrity (wrong damage mechanism, defect found but not fixed)
4. Operating procedures and safe operating limits (absent, outdated, or bypassed)
5. Incident investigation and action tracking (precursors not resolved)
6. Process safety information (P&IDs, reactivity data, materials of construction)
7. Contractor management (selection on cost, no oversight, language barriers)
8. Pre-startup safety review (compressed under schedule pressure)
9. Emergency planning and response (accountability, community notification, detection)

## Hazard classes and their signature failure

- **Reactive / runaway chemistry:** hazard unrecognized; relief sized for the
  wrong reaction; SADT and runaway are mass-dependent, so bench data is non-
  conservative at scale.
- **Combustible dust:** accumulation in concealed and elevated spaces; housekeeping
  treated as a chore rather than an engineering control; no Dust Hazard Analysis;
  a primary event lofts dust for a far larger secondary explosion.
- **Flammable vapor / vapor cloud explosion:** loss of containment plus no remote
  isolation plus an ignition source that is always findable; chasing the spark is
  the wrong question, not releasing the cloud is the only reliable answer.
- **Toxic gas release (H2S, chlorine, ammonia, HF):** detection absent or
  nonfunctional; isolation requires approaching the release; community in range.
- **Asphyxiation (nitrogen, inert gas, confined space):** the hazard gives no
  warning to the senses; written confined-space programs fail on execution; would-
  be rescuers become the next victims.
- **Overpressure / mechanical failure:** vessels without relief, without ASME
  certification, or beyond safe operating life; protective actions (closing a
  valve, plugging a vent) that create a worse trapped condition.
- **Hot work:** permit treated as a signature ritual; no atmosphere testing in the
  actual hazard zone; work near tanks and lines that were assumed clean or empty.

## Recommendation archetypes (strongest first)

The archive consistently shows administrative fixes failing and engineered or
inherent fixes holding. Prefer, in order:
1. **Eliminate or substitute** the hazard (inherently safer design, smaller
   inventory, less reactive material, relocate people out of the blast zone).
2. **Engineer it out** (remote isolation valves, properly sized relief, hard
   interlocks that cannot be bypassed with a hose, gas detection tied to action).
3. **Strengthen management systems** (PHA scope, MOC triggers, mechanical-integrity
   damage mechanisms, action-item tracking with deadlines).
4. **Administrative and PPE** last, and never as the only barrier for a hazard with
   catastrophic consequences.

## The transferable close (Monday-morning checklist pattern)

Every teardown ends with a few plant-agnostic checks. The durable ones from this
archive:
- Where does our dust, vapor, or trapped energy actually go, and who looked?
- Which serious hazard is guarded only by a person being perfect?
- Which near miss did we file as "not us," and is any corrective action overdue?
- What scenario was each relief device and alarm actually sized and located for?
- Who is inside our worst credible consequence radius right now?
