# RentEase deployment helpers

This folder holds everything needed to publish the application. Nothing here
contains credentials.

## Free hosting options

| Host | Works? | Notes |
|---|---|---|
| **Render** (free web service) | Yes | Python runtime, `render.yaml` included. Free instances sleep after 15 min. |
| **Railway** | Yes | Detects `Procfile`; needs a card on file. |
| **Fly.io** | Yes | Needs the `fly` CLI and a card. |
| **GitHub Pages** | **No** | Pages serves static files only. This app is PHP; it needs a runtime. |

GitHub Pages cannot host this project — it serves HTML/CSS/JS with no PHP
interpreter. The repository can still hold the source, with Render doing the
hosting.

## Render (the path of least friction)

1. Push this repository to GitHub.
2. On <https://dashboard.render.com> choose **New → Blueprint**.
3. Select the repository. Render reads `render.yaml` and provisions the
   service automatically.
4. The first build takes about two minutes. The URL is shown when it goes live.

Manual alternative: **New → Web Service**, set

```
Runtime:     Python 3
Build:       echo "no build step"
Start:       python3 runtime/router.py
```

The app uses SQLite automatically when MySQL is absent — `config/db.php`
falls back, creates `database/rentease.sqlite` and seeds it on first request.
No database service or environment variables are required.

## Seeded accounts

| Role | Email | Password |
|---|---|---|
| Owner | `ragav.owner@rentease.in` | `rent@1234` |
| Owner | `meera.owner@rentease.in` | `rent@1234` |
| Tenant | `arjun.tenant@rentease.in` | `rent@1234` |
| Tenant | `divya.tenant@rentease.in` | `rent@1234` |
| Tenant | `karthik.tenant@rentease.in` | `rent@1234` |

## Caveat: free-tier persistence

Render's free filesystem is ephemeral. The SQLite file is rebuilt from
`database/seed_sqlite.sql` whenever the instance restarts (roughly after 15
minutes idle), so **records created through the UI do not survive a restart**.
That is fine for a demonstration. For durable data, point `config/db.php` at a
hosted MySQL (PlanetScale, Aiven, Railway MySQL) instead.
