# Credential rotation runbook

Ordered by urgency. Items 1–3 were the active exposures — credentials pasted into a
chat transcript or committed to git. **1 and 3 are now closed** (see each item);
**item 2 is still open**, and item 4 is gated on the fsc-dashboard cutover.

Ground rule throughout: set new values interactively (`wrangler secret put`
prompts; dashboard fields) — never paste a secret into a command line or a
commit. Revoke the old value only after the new one is confirmed working.

---

## 1. Cloudflare "CF Master Token" — ✅ ROTATED (reported 2026-09-13)

Charlie confirmed a least-privilege token replaced the masters. Its value lives in
**1Password → `FSC-infra` → `Cloudflare API`** — the only copy, since Cloudflare
shows a token secret once and never again (registry §7).

**Reported, not verified from a session here.** No session in this repo has held a
`CLOUDFLARE_API_TOKEN`, and the Cloudflare MCP tools cover Workers, D1, KV and R2 —
not token management. Two things are still worth a look from a shell that has the
token, and both are cheap:

- the new token's id and actual scopes
- that the `site-admin` repo secret `CLOUDFLARE_API_TOKEN` holds the new value, not
  a master left in place — one green deploy run proves it

Closing this also closed audit item A2 (deploy token needs Secrets Store read) and
retired the never-used second master token.

### What this was, and why it is written down

The account API token had been pasted into a chat transcript. It was a
**full-account master token**: Secrets Store write, Workers Scripts write, Account
API Tokens write, Access write, DNS, Email Routing — total control of the account.
Two tokens carried the name "CF Master Token" (ids `d2fbf2c3…` used, `b3a2b3be…`
never used), plus an older `cfut_`-prefixed token also pasted.

The scoping that replaced it: Workers Scripts (edit), Secrets Store (read), D1
(edit), R2 (edit), Vectorize (edit), Workers AI, Account Settings (read) — which is
everything the deploys and the audit session actually exercised. Keep that list; it
is the answer to "what scopes does the next token need."

Either superseded id showing up in a config or workflow after this is a leftover to
clean up, not a working credential to keep. Rotation procedure lives in
`rotation-sops.md` → "`CLOUDFLARE_API_TOKEN`".

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

**Still gated as of 2026-09-13, and the gate is one action.** Checked against the
Netlify account that day: `site-admin-fsc` is live, claimed, current deploy `ready`,
and carries no password or SSO gate. Cloudflare's side is up —
`dashboard.florencescservices.com` is Access-gated — so what stands between here and
a clean rotation is **deleting the Netlify site**, not building anything further.
`florence-dashboard-proxy` is also still in the account (C5 says delete it).

Worth stating plainly because the belief runs the other way: Charlie's recollection
on 2026-09-13 was that Netlify was already out of the picture. It is not. Nine
projects are live (registry §6). Check the account, not the memory of the cutover.

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

## Repo visibility — READ THIS BEFORE ADDING ANYTHING HERE

⚠️ **This section's premise was wrong, and wrong in the direction that matters.
Corrected 2026-09-13.**

It used to say `cball8475/skills` was the only private repo, "which is why this
file, and any document naming live exposures, belongs here." **`cball8475/skills`
is PUBLIC.** It is a fork of `mattpocock/skills`, and a fork of a public repo is
public by default.

Verified anonymously, 2026-09-13: a no-auth request for
`raw.githubusercontent.com/cball8475/skills/main/skills/personal/fsc-credentials/references/rotation-status.md`
returns **200** and serves this file, while the same request against
`before-human-error`, `EATON` and `florence-crm-api` returns **404**. The 404s are
the control that makes the 200 mean something.

| Repo | Visibility (2026-09-13) |
|---|---|
| **`cball8475/skills`** | **PUBLIC — and it holds this file** |
| `site-admin` | PUBLIC |
| `LWVNewportCounty` | PUBLIC |
| `budget-guru-narrative` | PUBLIC |
| `cball8475.github.io` | public — user Pages site, must stay |
| `EATON` | **private** — changed since 2026-07-25 |
| `florence-crm-api` | private |
| `before-human-error` | private |

Two things follow, and the second is the one that changes behaviour.

**Treat everything in this directory as published.** Not secret values — there are
none here, and a shape scan confirms it — but the map: account and database ids,
the worker inventory, token ids, and an ordered list of which exposures are still
open. Making the repo private reduces further reading; it is not a retraction, and
because this is a fork, commits pushed while it was public can stay reachable
through the fork network.

**"Put it in the private repo" is not a placement rule that works here.** Until the
visibility is actually changed *and* re-verified with the no-auth check above, do
not add exposure detail to this directory believing it is unpublished.

### What the old section got right

EATON *was* public when the 2026-07-25 audit ran. So the audit's finding stands:
`site-admin/kb/fsc-memory.md` claimed the EATON bearer lived safely in a "private"
EATON repo, and the 2026-07-23 rotation moved that value from one public location
to another. The bearer was readable on GitHub for that window, which is why item 3
was a rotation and not housekeeping. **EATON is private now** — that recommendation
has been carried out.

Also still open from that audit: the EATON repo carries `claude.md` with Charlie's
employee ID, cost centre, work email and named succession details about a
colleague, plus `kb/` files about coworkers. Going private limits who can read it
now, but anything published during the public window is already out — a personnel
privacy matter independent of any secret.

**Still recommended:** make `site-admin` private (it reports `has_pages: false`, so
no hosting impact), and decide on `cball8475/skills` — which, holding this file, is
the more urgent of the two. `cball8475.github.io` must stay public, and
`LWVNewportCounty` likely serves the league site from Pages.

Note that removing a file from a public repo does not remove it from history —
these values are already published. Rotation is the remediation; relocation only
stops the bleeding.
