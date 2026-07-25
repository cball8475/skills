# FSC / EATON Credential Registry

**Verified by audit 2026-07-25.** Status column reflects what was actually tested that
day, not what was assumed.

**This file stores names and locations only — never values.** The previous version of
this skill cached a CRM bearer inline; the live token was rotated out from under it and
every task that used the cached value failed with a 401 while the skill reported
success. Names drift slowly, values drift silently. Look values up at the source.

Status legend: ✅ verified working · ⚠️ present but flagged · ❌ missing or broken ·
⏳ needs a dashboard check only Charlie can do

---

## 0. Non-secret identifiers (safe to reference inline)

These appear in dashboard URLs and config files. They are not credentials.

| Item | Value |
|---|---|
| Cloudflare Account ID | `37821191a8c1419e055c2c0a30546589` |
| D1 — florence-crm | `50e1fc12-682d-4d58-8506-93687a10dc36` |
| D1 — eaton-ehs-dashboard | `62ce85d7-0cc1-4832-aa57-d5b09ceaa132` |
| Secrets Store (EATON_TOKEN) | store `80c48360a0e54dd69425da2dfbde21ad` |
| Netlify Site ID (site-admin-fsc) | `18eefea7-8ee6-4e49-ad55-5896060f9be1` |
| CRM API base (custom domain) | `https://api.florencescservices.com` |
| EATON API base | `https://eaton-ehs-api.cball8475.workers.dev` |
| Google Ads account | `606-311-1549` |
| GA4 Property / account email | `529438443` / `charlieflorencescservices@gmail.com` |
| Windsor.ai account | `florence_sc_services_llc` |
| Twilio FROM (SMS) / toll-free | `(843) 773-4140` / `(833) 968-3306` |
| CallRail company | `322241453` |

---

## 1. Worker secrets

Cloudflare Worker secrets are **write-only by design** — you can confirm a name exists,
never read a value back.

**`wrangler secret list --name <worker>` is the only way to enumerate names**, and it
needs `CLOUDFLARE_API_TOKEN` in the environment. The Cloudflare MCP
`workers_get_worker` tool does **not** list bindings or secrets — it returns only the
script's name and id. (The old version of this skill claimed otherwise, which is why
the 2026-07-25 audit could not enumerate secrets and had to prove everything
functionally instead.)

### florence-crm-api

| Secret | Status (2026-07-25) | Notes |
|---|---|---|
| `API_TOKEN` | ⚠️ works, **but public** | Bearer for the CRM API. See "Known exposure" below |
| `GOOGLE_ADS_CLIENT_ID` | ✅ | OAuth for Ads + GSC |
| `GOOGLE_ADS_CLIENT_SECRET` | ✅ | |
| `GOOGLE_ADS_REFRESH_TOKEN` | ✅ | |
| `GOOGLE_ADS_DEVELOPER_TOKEN` | ✅ | `/ads/metrics` 200; spend currently zero |
| `TWILIO_ACCOUNT_SID` | ✅ | Proven via `lead_events.owner_alert` → `sms.sent:true` |
| `TWILIO_AUTH_TOKEN` | ✅ | Same |
| `GITHUB_TOKEN` | ⏳ | Required by `/github-push` + `/github-inject-pixel` (503 without). **Record PAT expiry** |
| `MERCURY_WEBHOOK_SECRET` | ⚠️ ⏳ | `ENFORCE_MERCURY_SIG = false` in source — signature checking is dead code, the secret is decorative. Decide: enforce or drop |
| `RESEND_API_KEY` | ❌ not set — **and not needed** | Superseded by the `MAILER` binding, which is confirmed delivering (`owner_alert` → `email.sent:true, via:"mailer"`). Do not "fix" this by adding the key without deciding which path owns owner-alert email |

Plain vars: `LEAD_ALERT_FROM`, `LEAD_ALERT_TO`, `OPERATOR_PHONE`.
Bindings: `DB` (D1 florence-crm), `MAILER` (service → `florence-auto-outreach-emails`,
entrypoint `Mailer`). Cron: `0 6 * * *` (SEO snapshot).

### eaton-ehs-api

| Secret | Status | Notes |
|---|---|---|
| `AUTH_TOKEN` (Secrets Store → `EATON_TOKEN`) | ✅ | Primary bearer. `/stats` 200 with, 401 without |
| `API_TOKEN` | ⏳ | Fallback bearer; can't be isolated externally while Secrets Store works |
| `ANTHROPIC_API_KEY` | ✅ | `/otter/extract` returned real structured tasks |
| `RESEND_API_KEY` | ⚠️ indirect | `/digest/preview` 200, but preview builds without touching Resend. Confirm via Resend dashboard activity |
| `GITHUB_BACKUP_TOKEN` | ✅ | `infra/backups/auto/d1-export-2026-07-25.json.gz` present. **Record PAT expiry** |

Vars: `GIT_SHA` (verified — `/health` reported `7d64c90`, matching main),
`DIGEST_FROM`, `DIGEST_TO`, `BACKUP_REPO`, `BACKUP_BRANCH`.
Bindings: `DB`, `AI`, `VECTORIZE` (eaton-memory). Crons: `0 14 * * 5` (Friday digest),
`0 12 * * 1` (Monday backup).

### d1-backup / kb-search

| Worker | Secret | Status |
|---|---|---|
| d1-backup | `API_TOKEN` | ✅ present — synced from repo secret `BACKUP_API_TOKEN` |
| kb-search | `API_TOKEN` | ✅ present — synced from repo secret `KB_API_TOKEN` |

Verified by sync-proof: both deploy workflows `exit 1` when their repo secret is
absent, and both ran green on 2026-07-25. Both endpoints also return 401
unauthenticated, confirming they fail closed. An authenticated 200 was not run — the
repo-secret values are write-only.

d1-backup: var `RETENTION_DAYS`; bindings 5× D1 (`DB_EATON`, `DB_CRM`, `DB_FAMILY`,
`DB_BHE`, `DB_TINY`) + R2 `BACKUPS`.
kb-search: var `EMBED_MODEL`; bindings `DB`, `AI`, `VEC` (Vectorize eaton-kb).

### fsc-dashboard (cutover in flight — not yet live as of 2026-07-25)

Serves the site-admin SPA and proxies its CRM calls so the bearer stays
server-side. Replaces the Netlify-hosted dashboard. Config lives at the
**site-admin repo root** `wrangler.toml` (not under `worker/`) because it serves
this repo's `./dist` build output.

| Secret | Location | Notes |
|---|---|---|
| `CRM_API_TOKEN` | Secrets Store, store `80c48360a0e54dd69425da2dfbde21ad` | ✅ **already exists** (confirmed 2026-07-25, comment "Shared FSC CRM…"). Bound as `CRM_API_TOKEN`; read per-request via `await env.CRM_API_TOKEN.get()`, so a rotation applies with no redeploy. ⚠️ **value vintage unverified** — see below |

Store `80c48360a0e54dd69425da2dfbde21ad` contains exactly two secrets (2/100):
`CRM_API_TOKEN` and `EATON_TOKEN`.

⚠️ **The CRM bearer now exists in three places** — florence-crm-api's `API_TOKEN`
worker secret, Netlify's `VITE_CRM_API_TOKEN`, and Secrets Store `CRM_API_TOKEN`.
Secrets Store values cannot be read back, so there is no way to confirm the third
matches the first without using it. Given that a fourth copy (cached in this skill)
had already gone stale unnoticed, treat the Secrets Store copy as unverified until
a rotation sets both deliberately. Symptom of a mismatch: the dashboard returns 401
through the proxy — a 503 means the binding failed, a 401 means the bearer resolved
but the CRM rejected it.

Its comment says "Shared", which implies another consumer may bind it. Check the
secret's bindings before rotating.

Vars: `CRM_ORIGIN` (`https://api.florencescservices.com`), `REQUIRE_ACCESS`
(`"false"` until the Cloudflare Access policy is verified). Bindings: `ASSETS`.
Route: `dashboard.florencescservices.com` (custom domain, DNS auto-created).

The deploying `CLOUDFLARE_API_TOKEN` needs **Secrets Store (read)** in addition to
Workers Scripts (edit), or every `/api` call returns 503.

Cutover steps are in `site-admin/docs/dashboard-deploy.md`. Until step 7 of that
runbook deletes the Netlify site, the old bundle with the embedded bearer is still
being served and bypasses Access — treat the exposure below as live until then.

### email-reply-ingest

✅ No secrets, working. 22 `inbound_nonprospect` rows on 2026-07-25 (newest 15:01:24)
prove the Email Routing rule targets this worker and D1 writes succeed.
Var: `FORWARD_TO` (defaults to `cball8475@gmail.com`). Binding: `DB` (florence-crm).

---

## 2. GitHub Actions repo secrets

Repo → Settings → Secrets and variables → Actions. **Remote Claude sessions cannot
read or set these** — the proxy blocks the Actions-secrets endpoints. Presence is
proven indirectly by whether a guarded workflow ran green.

| Repo | Secret | Status |
|---|---|---|
| site-admin | `CLOUDFLARE_API_TOKEN` | ✅ deploys green 2026-07-25 |
| site-admin | `BACKUP_API_TOKEN` | ✅ (workflow `exit 1` without it) |
| site-admin | `KB_API_TOKEN` | ✅ (same) |
| site-admin | `RESEND_API_KEY` | ❌ not set — intentional, see MAILER note above |
| EATON | `CLOUDFLARE_API_TOKEN` | ✅ eaton-ehs-api deploy green 2026-07-25 |
| LWVNewportCounty | `MEMBER_PASSWORD` | ✅ portal build asserts non-empty and ran green |

⏳ Scope check still owed on both `CLOUDFLARE_API_TOKEN` copies: Workers Scripts
(edit), D1 (edit), R2 (edit), Vectorize (edit), Workers AI, Secrets Store (read).

---

## 3. Netlify environment variables (site-admin-fsc)

Site configuration → Environment variables. `VITE_`-prefixed vars are **inlined into
the public JS bundle at build time** — they are published, not stored. Changing one
requires a redeploy.

| Variable | Status |
|---|---|
| `VITE_CRM_API_URL` | ✅ set → `https://api.florencescservices.com` |
| `VITE_CRM_API_TOKEN` | ⚠️ set and matches the worker `API_TOKEN` — **and is public** |
| `VITE_GOOGLE_PLACES_KEY` | ⚠️ set, `AIza…` key published in the bundle. Needs HTTP-referrer restriction |
| `VITE_GITHUB_TOKEN` | ❌ **orphaned — delete it** |

⚠️ **This whole section is being retired.** Once the fsc-dashboard cutover is done,
the dashboard builds in GitHub Actions and deploys to Cloudflare, and Netlify holds
nothing. Of these four, only `VITE_GOOGLE_PLACES_KEY` carries over — as a repo secret
in site-admin, with its HTTP-referrer restriction moved to
`dashboard.florencescservices.com`. The other three should not be recreated anywhere.

`VITE_GITHUB_TOKEN` has zero references in `src/` and no PAT appears in the built
bundle. Dashboard GitHub features go through the worker's `GITHUB_TOKEN` secret. A PAT
inlined into a public bundle would be far worse than the CRM token; remove the variable
so a future build can't start publishing it.

Correct names matter here: source reads **`VITE_CRM_API_TOKEN`** at three call sites.
`VITE_API_TOKEN` is only a non-PROD fallback in `GoogleAdsTile.jsx`.

### Known exposure — CRM bearer is public

The CRM bearer is downloadable by anyone who loads
`https://site-admin-fsc.netlify.app`. The audit extracted it unauthenticated and
pulled 200s from `/prospects`, `/ads/metrics`, `/seo/metrics`, `/gsc/metrics`.

Rotating alone does not fix this — the replacement is re-published on the next build.

**Fix is built, cutover pending:** the `fsc-dashboard` worker above serves the SPA
and proxies `/api/*` with the bearer from Secrets Store, and Cloudflare Access gates
the hostname. Prod is pinned to same-origin `/api` with no token in all three call
sites, and the deploy workflow fails the build if a `VITE_*_TOKEN` is in the
environment or a credential shape appears in `dist/`.

Two things still make the exposure live until the runbook is finished:

1. `site-admin-fsc.netlify.app` still answers and still serves the old bundle. It
   also sits outside Cloudflare's edge, so Access cannot gate it. **Deleting it is
   what actually closes the hole** — not deploying the replacement.
2. The current bearer is burned and still valid. Rotate after the new path is
   verified (runbook step 8).

Root cause worth remembering: the client code was already correct — it fell back to
`/api` and omitted the auth header when no token was set. Setting
`VITE_CRM_API_URL` + `VITE_CRM_API_TOKEN` in Netlify overrode that. The lesson is
that a `VITE_`-prefixed var is a publishing decision, not a configuration one.

---

## 4. Local development

Never hardcode secrets. Confirm `.gitignore` covers `.env`, `.env.local`,
`.env.*.local`, `.dev.vars` **before** creating the file.

| Project | Mechanism |
|---|---|
| site-admin (Vite) | `.env` with `VITE_` prefix — remember these become public at build |
| Cloudflare Workers | `.dev.vars` in the worker dir, read by `wrangler dev`, never deployed |
| Node one-offs | `dotenv` |

`.dev.vars` holds only the names the worker actually reads — fill values from the
source of record, and do not copy them into any committed file:

```
API_TOKEN=
ANTHROPIC_API_KEY=
RESEND_API_KEY=
```

---

## 5. Third-party accounts

Anthropic · Resend (domain verified: florencescservices.com) · Google Cloud OAuth app
(Ads + GSC scopes) · Twilio · Mercury (webhook) · GitHub PATs ×2 (crm `GITHUB_TOKEN`,
eaton `GITHUB_BACKUP_TOKEN` — both expire, record the dates) · Netlify · Cloudflare
(D1, R2, Vectorize, AI, Secrets Store) · StatiCrypt member password (⏳ who else holds
it?).

SendGrid, Stripe, and Wave are **not** part of this stack. Earlier versions of this
skill routed to `dashboard.sendgrid.com` and put `SENDGRID_API_KEY` in the `.dev.vars`
template; all email is Resend. Do not reintroduce them.

---

## 6. Open gaps

- **Inventory is incomplete.** The Cloudflare account holds **16** workers; only 5 are
  documented here or in `site-admin/docs/credential-audit.md`. Undocumented:
  `florence-outreach`, `florence-auto-outreach-emails` (the `MAILER` target — holds a
  working Resend key, confirmed sending 2026-07-24), `florence-lead-capture`,
  `florence-lead-followup`, `florence-utm-inject`, `florence-dashboard-proxy` (404s on
  every path — likely dead, retire it), `ball-family-api`, `ball-family-ingest`,
  `fsc-api-canary`, `deal-or-no-deal`, `tiny-mountain-65c7`. Several send email or take
  webhooks, so several hold secrets. `florence-auto-outreach-emails` has no source in
  any of the five repos. `florence-dashboard-proxy` is slated for deletion as part of
  the fsc-dashboard cutover — it was an unfinished attempt at the same proxy.
- **`florence-health-check` does not exist.** A previous version of this skill carried
  standing `TWILIO_*` "NOT SET" flags for it. No such worker is in the account.
- **`CLOUDFLARE_API_TOKEN` is not in the Claude Code cloud session env** — confirmed
  absent on both 2026-07-25 sessions, so `wrangler` cannot authenticate remotely.
  `EATON/infra/env.sh` claims every session exports it automatically; that comment is
  wrong.
- **EATON bearer is committed in plaintext** at `EATON/infra/env.sh`, duplicating the
  Secrets Store `EATON_TOKEN` and relying on manual sync. Git history retains it —
  treat as compromised and rotate, or accept and document.
