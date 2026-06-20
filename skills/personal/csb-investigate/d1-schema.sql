-- CSB investigation schema (Cloudflare D1 / SQLite-compatible).
-- Optional persistence: apply only to an existing database. Do not provision a
-- database from this file. Safe to run repeatedly (IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS incidents (
    id              TEXT PRIMARY KEY,            -- slug or report number
    name            TEXT NOT NULL,
    company         TEXT,
    location        TEXT,
    incident_date   TEXT,                        -- ISO 8601
    materials       TEXT,                        -- chemicals/materials involved
    consequences    TEXT,                        -- fatalities/injuries/damage/env
    report_no       TEXT,
    risk_band       TEXT,                        -- Low/Moderate/High/Critical
    product_tier    TEXT,                        -- note/digest/full/hazard
    status          TEXT DEFAULT 'open',
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS timeline_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    event_time  TEXT,
    phase       TEXT,                            -- pre-incident/incident/response/consequences
    description TEXT NOT NULL,
    evidence    TEXT
);

CREATE TABLE IF NOT EXISTS causal_factors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    factor_type TEXT,                            -- immediate/contributing
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS root_causes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    description TEXT NOT NULL                     -- management-system deficiency
);

CREATE TABLE IF NOT EXISTS findings (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recommendations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    ref         TEXT,                            -- e.g., R-1
    recipient   TEXT,                            -- company/regulator/industry
    description TEXT NOT NULL,
    addresses   TEXT                             -- finding/root cause it answers
);

CREATE TABLE IF NOT EXISTS corrective_actions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id         TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    ref                 TEXT,                    -- e.g., CA-1
    description         TEXT NOT NULL,
    addresses           TEXT,                    -- finding/root cause/recommendation
    control_tier        TEXT,                    -- eliminate/substitute/engineering/admin/PPE
    value_add_rationale TEXT,                    -- why it is value-added
    owner               TEXT,
    target_impl_date    TEXT,
    implemented_date    TEXT,
    status              TEXT DEFAULT 'open'      -- open/implemented/verified/closed
);

CREATE TABLE IF NOT EXISTS effectiveness_checks (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    corrective_action_id INTEGER NOT NULL REFERENCES corrective_actions(id) ON DELETE CASCADE,
    smart_specific      TEXT,
    method              TEXT,                    -- audit/measurement/observation/records
    pass_fail_criteria  TEXT NOT NULL,
    scheduled_run_date  TEXT,                    -- when to run after implementation
    trigger_event       TEXT,                    -- alternative/additional trigger
    run_date            TEXT,
    result              TEXT,                    -- pass/fail
    status              TEXT DEFAULT 'scheduled' -- scheduled/passed/failed/re-opened
);

CREATE INDEX IF NOT EXISTS idx_timeline_incident   ON timeline_events(incident_id);
CREATE INDEX IF NOT EXISTS idx_causal_incident     ON causal_factors(incident_id);
CREATE INDEX IF NOT EXISTS idx_root_incident       ON root_causes(incident_id);
CREATE INDEX IF NOT EXISTS idx_findings_incident   ON findings(incident_id);
CREATE INDEX IF NOT EXISTS idx_recs_incident       ON recommendations(incident_id);
CREATE INDEX IF NOT EXISTS idx_ca_incident         ON corrective_actions(incident_id);
CREATE INDEX IF NOT EXISTS idx_effchk_ca           ON effectiveness_checks(corrective_action_id);
CREATE INDEX IF NOT EXISTS idx_effchk_due          ON effectiveness_checks(scheduled_run_date);
