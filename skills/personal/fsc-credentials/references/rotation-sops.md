# Rotation SOPs

One procedure per credential. Two rules apply to all of them:

1. **Never pipe a secret through a command that logs it.** Use `wrangler secret put`
   interactively, or paste in a dashboard field.
2. **Revoke the old value only after the new one is confirmed live.** Reverse that
   order and you get an outage instead of a rotation.

Rotation dates belong in `registry.md`'s status column, not here.

---

## florence-crm-api `API_TOKEN` (the CRM bearer)

⚠️ Read `registry.md` → "Known exposure" first, and check whether the fsc-dashboard
cutover (`site-admin/docs/dashboard-deploy.md`) is finished — the procedure differs.

**After cutover** (Netlify deleted, fsc-dashboard live) — two places, no rebuild:

1. `npx wrangler secret put API_TOKEN --name florence-crm-api`
2. `npx wrangler secrets-store secret update 80c48360a0e54dd69425da2dfbde21ad`
   (secret `CRM_API_TOKEN`) — same value
3. Confirm: dashboard tiles populate, and the **old** token now returns 401 against
   `https://api.florencescservices.com/prospects`

No redeploy: the worker reads Secrets Store per request.

**Before cutover** — the dashboard still carries the token, so it is three places and
a rebuild, and the new value is published again on the next build. Prefer finishing
the cutover to rotating in this state:

1. `npx wrangler secret put API_TOKEN --name florence-crm-api`
2. Netlify → site-admin-fsc → Environment variables → `VITE_CRM_API_TOKEN`
3. Redeploy the dashboard — Vite inlines at build time, so an env change alone does
   nothing
4. Confirm with bearer → 200, without → 401, and that tiles populate

---

## Worker secret, general case

```bash
export XDG_CONFIG_HOME="$HOME/.wrangler-config"
npx wrangler secret put SECRET_NAME --name worker-name   # prompts; paste, Enter
npx wrangler secret list --name worker-name              # confirm the name appears
```

Needs `CLOUDFLARE_API_TOKEN` in the environment — **not available in Claude Code cloud
sessions** (see registry §6). From a cloud session, either do it in the dashboard
(Workers & Pages → worker → Settings → Variables → Secrets) or let the deploy workflow
sync it.

If a worker reads the secret at startup, verify with `npx wrangler tail worker-name` and
a single request. **Never trigger a cron to test** — it advances real sequences and
snapshots. Use a health or preview endpoint.

---

## Secrets-Store secrets (EATON bearer)

`EATON_TOKEN` lives in Cloudflare Secrets Store (store `80c48360a0e54dd69425da2dfbde21ad`)
and is bound into eaton-ehs-api as `AUTH_TOKEN`. It is **duplicated in plaintext** at
`EATON/infra/env.sh`, whose own comment requires manual sync.

1. Update the Secrets Store value (dashboard → Secrets Store).
2. Update `EATON/infra/env.sh` to match, or — preferred — remove the value from the file
   and have it read from the environment, so the duplication ends.
3. Confirm: `/stats` 200 with the new bearer, 401 without.
4. Because the old value is in git history, treat any rotation here as a
   compromise-response: the point is that the committed value stops being valid.

---

## Tokens synced from GitHub Actions secrets

`BACKUP_API_TOKEN` → d1-backup `API_TOKEN`, `KB_API_TOKEN` → kb-search `API_TOKEN`.
The workflow is the source of truth; don't set these on the worker by hand or the two
drift.

1. Repo → Settings → Secrets and variables → Actions → update the secret.
2. Re-run the matching workflow (`deploy-d1-backup.yml` / `deploy-kb-search.yml`).
3. Both workflows `exit 1` if the secret is empty, so a green run is the confirmation.
4. Functional check: `GET /backups` / `GET /search?q=test` with the new bearer → 200;
   no-auth → 401.

---

## GitHub PATs

Two exist: crm `GITHUB_TOKEN` (dashboard GitHub features) and eaton
`GITHUB_BACKUP_TOKEN` (Monday D1 backup push, `repo` scope). Both expire — record
expiry dates in `registry.md` and rotate before, not after.

1. GitHub → Settings → Developer settings → Personal access tokens → regenerate.
2. Set on the worker that uses it (see general case above).
3. Confirm: for `GITHUB_BACKUP_TOKEN`, the newest
   `EATON/infra/backups/auto/d1-export-*.json.gz` should be ≤7 days old after the next
   Monday run. For crm `GITHUB_TOKEN`, `/github-push` returns 503 when it's missing.
4. Revoke the old PAT.

Push protection rejects commits containing `cfat_` Cloudflare tokens — never try to
commit one as a workaround.

---

## Google OAuth (Ads + GSC)

Four secrets move together: `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`,
`GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_DEVELOPER_TOKEN`. A refresh token is bound to
the client that issued it — rotating the client secret invalidates it, so re-mint both.

1. Google Cloud Console → APIs & Services → Credentials for the OAuth app.
2. Re-consent as `charlieflorencescservices@gmail.com` to mint a refresh token.
3. Set all changed secrets on florence-crm-api.
4. Confirm: `/ads/metrics?days=7` → 200 and `/seo/metrics?days=7` → 200. A well-formed
   200 with zero spend means the credentials work and there's no active spend — that is
   not a credential failure.

---

## Resend

One Resend account serves the eaton weekly digest and the outreach mailer. Domain
`florencescservices.com` is verified.

1. Resend dashboard → API Keys → create the replacement.
2. Set on the workers that read it (currently eaton-ehs-api, and
   `florence-auto-outreach-emails` which backs the `MAILER` binding).
3. **A send-test is forbidden during an audit.** Verify from Resend's recent-activity
   view, or read `lead_events.owner_alert` → `email.sent` / `outreach_log.email_sent`.
4. Delete the old key.

---

## Twilio

1. Twilio Console → rotate the auth token (SID is stable).
2. Set `TWILIO_AUTH_TOKEN` on florence-crm-api.
3. **No test send.** Verify from Console message logs, or the next real lead's
   `lead_events.owner_alert` → `sms.sent:true`. Error 30034 there means a carrier drop,
   not a credential problem.

---

## StatiCrypt `MEMBER_PASSWORD`

Member-facing — rotating it locks out every member until they're told the new one.
Confirm distribution before rotating.

1. LWVNewportCounty → Settings → Secrets and variables → Actions → `MEMBER_PASSWORD`.
2. Re-run `update-member-portal.yml`. It refuses to build on an empty password and
   verifies the output is actually encrypted.
3. Confirm: open `lwvnewportcounty.org/members.html`, enter the new password, portal
   decrypts.

---

## Mercury `MERCURY_WEBHOOK_SECRET`

`ENFORCE_MERCURY_SIG = false` in florence-crm-api, so this secret currently gates
nothing — signature mismatches are computed and ignored. Decide whether to enforce
before treating a rotation as meaningful.

1. Mercury dashboard → webhook config → rotate the signing secret.
2. Set `MERCURY_WEBHOOK_SECRET` on florence-crm-api.
3. Inbound webhooks can't be probed from outside; confirm from Mercury's webhook
   delivery log.
