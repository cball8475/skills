# Credential rotation runbook

Ordered by urgency. Items 1–3 are active exposures — credentials pasted into a
chat transcript or committed to git. Do them first, today.

Ground rule throughout: set new values interactively (`wrangler secret put`
prompts; dashboard fields) — never paste a secret into a command line or a
commit. Revoke the old value only after the new one is confirmed working.

---

## 1. Cloudflare "CF Master Token" — EMERGENCY

The current account API token was pasted in chat. It is a **full-account master
token**: Secrets Store write, Workers Scripts write, Account API Tokens write,
Access write, DNS, Email Routing — total control of the account. Treat it as
compromised now.

There are **two** tokens named "CF Master Token" (ids `d2fbf2c3…` used today,
`b3a2b3be…` never used) plus an old `cfut_`-prefixed token also pasted. Rotate all
of them, and take the opportunity to stop using a master token in automation:

1. Zero Trust / dashboard → My Profile → **API Tokens**.
2. **Create one least-privilege token** for CI/deploys: Workers Scripts (edit),
   Secrets Store (read), D1 (edit), R2 (edit), Vectorize (edit), Workers AI,
   Account Settings (read). That is everything the deploys and this session's
   work actually used.
3. Put it in the site-admin repo secret `CLOUDFLARE_API_TOKEN`, and anywhere else
   a deploy token is configured.
4. **Roll (regenerate) or delete both "CF Master Token"s and the old `cfut_`
   token.** Nothing should keep a master-scoped token in automation.
5. Confirm a deploy still runs green with the new scoped token.

This single step also closes audit item A2 (deploy token needs Secrets Store
read) and retires the never-used second master token.

## 2. GitHub PAT `fsc-crm-api-push` — EMERGENCY

The `fsc-crm-api-push` fine-grained PAT was pasted in chat. It is live.

1. GitHub → Settings → Developer settings → Fine-grained tokens →
   `fsc-crm-api-push` → **Revoke**.
2. Regenerate a replacement with the same repo scope.
3. Set it on every worker that holds a GitHub PAT of this identity — at least
   `florence-crm-api.GITHUB_TOKEN`, and check `florence-lead-capture.GITHUB_TOKEN`:
   ```
   npx wrangler secret put GITHUB_TOKEN --name florence-crm-api
   npx wrangler secret put GITHUB_TOKEN --name florence-lead-capture
   ```
4. Confirm `/github-push` on florence-crm-api returns non-503.

While here, the sweep found **four** GitHub PATs on the account
(`florence-crm-api`, `florence-lead-capture`, `eaton-ehs-api.GITHUB_BACKUP_TOKEN`,
`tiny-mountain-65c7.Github_PAT`). Record each one's expiry; rotate any that are
shared or aging.

## 3. EATON bearer — ✅ DONE 2026-07-29

Rotated by the **Rotate EATON API token** workflow (EATON repo), run #1,
2026-07-29 01:13 UTC, green. It updated Secrets Store `EATON_TOKEN`, the
`API_TOKEN` worker fallback, and the D1 `app_config` self-serve copy in one
pass. Independently verified after the run: the leaked git-history value
returns **401**, the rotated value returns **200** end-to-end from a session.
`fsc-api-canary` needed nothing (reads Secrets Store). Future rotations: run
the workflow, never rotate by hand (see rotation-sops).

Still open from the original item, both optional:
- Local shells holding a pre-rotation `~/.fsc/eaton.token` will 401 until
  `eaton_refresh_token` (env.sh re-fetches from D1 automatically when
  `CLOUDFLARE_API_TOKEN` is present).
- History scrub (`git filter-repo --replace-text`) is now cosmetic — the
  published value is dead. Skip unless scrubbing anyway for item 5's reasons.

## 4. CRM bearer — public, and duplicated in six places

Do this **after** the fsc-dashboard cutover deletes the Netlify site (see
`dashboard-deploy.md` C2). Rotating before then breaks the live Netlify dashboard,
which still serves the old baked bearer.

The bearer exists in six places — four plain worker secrets, Secrets Store, and
Netlify:

| Location | How to set |
|---|---|
| florence-crm-api `API_TOKEN` (the inbound guard) | `wrangler secret put API_TOKEN --name florence-crm-api` |
| florence-dashboard-proxy `CRM_API_TOKEN` | delete this worker instead (C5) |
| florence-lead-capture `CRM_API_TOKEN` | `wrangler secret put CRM_API_TOKEN --name florence-lead-capture` |
| florence-auto-outreach-emails `CRM_API_TOKEN` | `wrangler secret put CRM_API_TOKEN --name florence-auto-outreach-emails` |
| Secrets Store `CRM_API_TOKEN` | `wrangler secrets-store secret update 80c48360… ` |
| Netlify `VITE_CRM_API_TOKEN` | gone once the site is deleted |

All must be set to the **same** new value in one pass, or a caller 401s. Miss one
and that path breaks silently.

### Making "rotate here once" actually true

The Secrets Store comment says rotate once. That only becomes true when every
consumer *reads* the Secrets Store binding instead of holding a plain copy —
`fsc-api-canary` already does (`env.CRM_TOKEN.get()`), and the new fsc-dashboard
does. To finish it:

- **florence-crm-api** (source is in this repo): change its inbound guard to
  validate against the Secrets Store value with an `API_TOKEN` fallback, exactly
  as `eaton-ehs-api` does for `AUTH_TOKEN`. Add the `[[secrets_store_secrets]]`
  binding to its `wrangler.toml`. Safe to do here because the fallback keeps the
  old value working during the transition. **Do the coordinated rotation above
  first**, so the Secrets Store value provably matches what callers send before
  the guard starts trusting it — otherwise a mismatch 401s everyone.
- **dashboard-proxy / lead-capture / auto-outreach-emails**: no source in any of
  the five repos, so this requires either recovering their source or editing
  deployed bundles. Not safe to do blind — lead-capture is the new-lead intake
  path. Recover source first, then convert `` `Bearer ${env.CRM_API_TOKEN}` `` to
  `Bearer ${await env.CRM_API_TOKEN.get()}` with the binding.

Until all four are migrated, rotation is a 5–6-place operation. A one-shot script
that `wrangler secret put`s the same value to each name makes it a single command
even before the migration.

---

## What can be automated vs. what needs you

- **Server-side-only rotations** (a value no human needs to hold) can be scripted
  with the account token. None of the above is purely server-side: each has a
  local shell, a GitHub side, or a Netlify side that needs the new value, and the
  standing rule is never to print a secret value into chat.
- **The account/GitHub rotations (1–2)** must be done in those dashboards — a
  Cloudflare token cannot revoke a GitHub PAT, and a token should not delete the
  token it is authenticating with.

Offer stands: once you have chosen a rotation window, the Cloudflare-side
`wrangler` steps in 3 and 4 can be run for you, driven interactively so no value
is printed — say the word and pass a fresh scoped token (not the master).

---

## Repo visibility — the reason this file lives here

**All five FSC/EATON GitHub repos are PUBLIC** (verified 2026-07-25 via the
repos API: `site-admin`, `EATON`, `cball8475.github.io`, `LWVNewportCounty`,
`budget-guru-narrative` all return `private: false`). `cball8475/skills` is the
**only private** repo — which is why this file, and any document naming live
exposures, belongs here and not in site-admin.

This corrects a load-bearing wrong assumption. `site-admin/kb/fsc-memory.md`
states the EATON bearer's new value "lives in the EATON repo `infra/env.sh`
(private repo) — never in this repo (public)." **EATON is not private.** The
2026-07-23 rotation, which was itself a response to that token leaking from a
public dashboard, moved the value from one public location to another. The bearer
has been readable on GitHub since. That is why item 3 of this runbook is urgent
rather than housekeeping.

Beyond credentials, the public EATON repo also carries `claude.md` with Charlie's
employee ID, cost centre, work email, and named succession details about a
colleague, plus `kb/` tribal-knowledge files about coworkers. That is a personnel
privacy exposure independent of any secret.

**Recommended:** make `site-admin` and `EATON` private. Caveats to check first —
`cball8475.github.io` must stay public (user Pages site), `LWVNewportCounty` likely
serves the league site from Pages, and EATON has GitHub Pages build runs, so if its
dashboard is served from Pages, going private needs a plan that supports private
Pages or a move to Cloudflare. site-admin reports `has_pages: false`, so it can be
made private with no hosting impact.

Note that removing a file from a public repo does not remove it from history —
these values are already published. Rotation is the remediation; relocation only
stops the bleeding.
