# Deploy RentEase

## One-click Render deploy (permanent link)

1. Sign in at <https://dashboard.render.com> with the GitHub account that owns this repo.
2. **New → Blueprint**
3. Choose **Ragav4488/Rent-Ease**
4. Render reads `render.yaml` (Docker runtime), builds, and gives a permanent
   `https://rentease-xxxx.onrender.com` URL.

Free instances sleep after 15 minutes idle; the first hit afterwards takes ~30s.

## Why Docker

Render has no native PHP runtime. `Dockerfile` uses `php:8.3-apache` with
`pdo_sqlite` + `pdo_mysql`.

## Why no database setup is needed

`config/db.php` tries MySQL first; when none is reachable it creates and seeds
`database/rentease.sqlite` on first request.

**Caveat:** the free-tier filesystem is ephemeral, so records created through
the UI reset when the instance restarts. Seed data always returns.

## Demo accounts

| Role | Email | Password |
|---|---|---|
| Owner | ragav.owner@rentease.in | rent@1234 |
| Tenant | arjun.tenant@rentease.in | rent@1234 |
