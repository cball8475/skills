---
name: fsc-credentials
description: Manages the full credential registry for Florence SC Services LLC infrastructure. Use this skill whenever any task requires a secret, API key, token, bearer token, or credential for any FSC system — including GitHub PAT, Cloudflare API token, CRM API bearer, Resend, Anthropic API key, Twilio, CallRail, Google Ads/GA4, Netlify, Windsor.ai, or Mercury. Also use when rotating, verifying, or debugging credential issues, or when a Worker deploy fails and secrets may be the cause. Trigger on any mention of "token", "secret", "API key", "PAT", "credentials", "auth", or "permission denied" in an FSC infrastructure context.
---

# FSC Credential Management

## Ground Rules

1. **Never print secret values in chat.** Reference by name only. To set a value, have
   Charlie paste it interactively (`wrangler secret put`) or into a dashboard field —
   never pipe it through a command that logs it.
2. **This skill does not store secret values.** `references/registry.md` holds names,
   locations, and how to obtain each credential. Look values up at the source of record
   every time. A cached value that has since been rotated is worse than no value at
   all: it fails with a plausible-looking 401 while the skill reports success. This has
   already happened once — an inline CRM bearer here went stale and was still being
   handed out.
3. **Cloudflare Worker secrets are write-only.** You can confirm a name exists, never
   read a value back. That is by design.
4. **Non-secret identifiers** (account IDs, database IDs, site IDs, phone numbers, GA4
   property) are in `references/registry.md` §0 and are safe to use inline.
5. **Never hardcode secrets in source.** Use `.env` / `.dev.vars` locally (gitignored),
   repo secrets for CI, Worker secrets for Cloudflare. A secret that reaches a commit is
   compromised — git history retains it. Rotate, don't just revert.
6. **`VITE_`-prefixed vars are published, not stored.** Vite inlines them into the
   public bundle at build time. Anything with that prefix is world-readable the moment
   it deploys.

---

## Step 1 — Identify what's needed

Determine which credential, which service or Worker needs it, and whether it exists.
Look up the exact name and location in `references/registry.md` — the status column
records what was last actually verified, and §6 lists known gaps.

---

## Step 2 — Verify

**Prefer a functional test over an existence check.** Existence proves a name is set;
only a functional test proves the value is right. The registry's status column was
built this way, after an existence-only view of the same infrastructure turned out to
be wrong in several places.

### Enumerating names

```bash
npx wrangler secret list --name worker-name
```

This is the **only** way to list Worker secret names. It requires
`CLOUDFLARE_API_TOKEN` in the environment, which **Claude Code cloud sessions do not
have** — verify before assuming, and fall back to functional tests or the dashboard.

The Cloudflare MCP `workers_get_worker` tool returns only the script's name and id. It
does **not** list bindings, vars, or secrets — do not rely on it for this.

### Verifying without side effects

Read-only proofs that worked on 2026-07-25, useful whenever a credential is suspect:

| Credential | Safe test |
|---|---|
| crm `API_TOKEN` | `GET /prospects` with bearer → 200; without → 401 |
| `GOOGLE_ADS_*` | `GET /ads/metrics?days=7` → 200 (exercises OAuth refresh + Ads read) |
| Google GSC | `GET /seo/metrics?days=7` → 200 |
| `TWILIO_*` | `lead_events.owner_alert` → `sms.sent` on the newest lead. **No test send** |
| Resend (either worker) | `outreach_log.email_sent`, or `owner_alert` → `email.sent`. **No test send** |
| eaton `AUTH_TOKEN` | `GET /stats` with bearer → 200; without → 401 |
| eaton `ANTHROPIC_API_KEY` | `POST /otter/extract` with a 2-line dummy transcript → 200 |
| eaton `RESEND_API_KEY` | `GET /digest/preview` builds without sending (indirect only) |
| eaton `GITHUB_BACKUP_TOKEN` | Newest `EATON/infra/backups/auto/d1-export-*.json.gz` ≤7 days old |
| Repo secrets | A guarded workflow running green — `deploy-d1-backup` / `deploy-kb-search` / `update-member-portal` all `exit 1` when their secret is empty |

Never trigger a cron to test a credential — it advances real sequences and snapshots.
Never `POST /digest/send`. Never send test SMS or email.

### Credentials only Charlie can source

Tell him exactly where to get it and where to put it — don't just say "go find it."

- `CLOUDFLARE_API_TOKEN` — Cloudflare → My Profile → API Tokens (also needed for local
  wrangler; absent from cloud sessions)
- GitHub Actions repo secrets — remote sessions cannot read or set these; the proxy
  blocks the Actions-secrets endpoints
- Google account / OAuth consent (Ads, GA4, GSC)
- Resend API key — Resend dashboard → API Keys
- Twilio auth token — Twilio Console
- Mercury credentials and webhook secret — mercury.com

### Self-serve credentials — never ask Charlie to paste these

- **EATON bearer** (2026-07-29+): D1 `app_config`, key `EATON_TOKEN`, db
  `62ce85d7-0cc1-4832-aa57-d5b09ceaa132`. `EATON/infra/env.sh` resolves it
  automatically (env var → `~/.fsc/eaton.token` → D1 fetch when
  `CLOUDFLARE_API_TOKEN` exists). Cloud sessions without any of those: read the
  row with Cloudflare MCP `d1_database_query`, write `~/.fsc/eaton.token`
  (mode 600), source env.sh again. On 401 after a rotation:
  `eaton_refresh_token`. Storing the bearer in D1 grants nothing new — D1
  access already implies full data access — and `/export` enumerates its
  tables, so backups never carry it.

---

## Step 3 — Set or rotate

Follow the per-service procedure in `references/rotation-sops.md`. General case:

```bash
export XDG_CONFIG_HOME="$HOME/.wrangler-config"
npx wrangler secret put SECRET_NAME --name worker-name   # prompts; paste, Enter
```

Dashboard path: Workers & Pages → worker → Settings → Variables → Secrets.

Two credentials are **two-place changes** — miss the second place and it silently
half-works:

- The CRM bearer must match across florence-crm-api `API_TOKEN` **and** Netlify
  `VITE_CRM_API_TOKEN` (plus a redeploy, since Vite inlines at build time).
- The EATON bearer is a **four-place change** (Secrets Store `EATON_TOKEN`,
  worker `API_TOKEN` fallback, D1 `app_config`, dashboard localStorage) — which
  is why it is never rotated by hand: run the **Rotate EATON API token**
  workflow in the EATON repo, which changes the first three atomically and
  verifies the old value is dead (see rotation-sops).

Tokens synced from repo secrets (`BACKUP_API_TOKEN`, `KB_API_TOKEN`) should be changed
in GitHub and re-synced by re-running the workflow — not set on the worker by hand, or
the two drift.

---

## Step 4 — Confirm, then revoke

1. Confirm the name appears in `wrangler secret list` (when you can run it).
2. Run the credential's functional test from the table above.
3. Only then revoke the old value.
4. Update the status column in `references/registry.md`.

---

## Reference files

- `references/registry.md` — every credential: name, location, verified status, and the
  open gaps (including the incomplete Worker inventory and the published CRM bearer)
- `references/rotation-sops.md` — per-service rotation procedures
