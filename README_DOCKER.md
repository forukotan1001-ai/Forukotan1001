# Docker development & CI notes — UEBA Security

This document explains how to run the UEBA Security platform locally with Docker and how the CI pipeline runs migrations and smoke-tests.

Quickstart (local)

1. Copy or create a local `.env` file with any secrets you need (do NOT commit real secrets).

2. Build and start services with compose:

```powershell
Set-Location -Path 'D:\UebaSecurityV2'
docker compose up --build
```

The compose setup starts three services:
- `db` — PostgreSQL (exposes host port 5433 -> container 5432)
- `redis` — Redis (exposes host port 6379)
- `web` — UEBA FastAPI app (exposes host port 8000)

By default the `web` service uses the following DATABASE_URL (compose internal DNS):

```
postgresql://postgres:${DB_PASSWORD:-example}@db:5432/ueba_security
```

If you want to run migrations manually outside the container:

```powershell
# after starting db and redis
docker compose run --rm -e DATABASE_URL=postgresql://postgres:example@db:5432/ueba_security web python infrastructure/02_auto_migration_on_startup.py
```

Skip migrations
- To skip automatic migration in the container entrypoint, set `SKIP_MIGRATIONS=1` in the environment or your `.env`.

CI behavior
- The GitHub Actions workflow builds the Docker image and scans it with Trivy.
- CI starts `db` and `redis` first, then runs migrations as a one-off inside the built `web` image:

```
docker compose up -d db redis
docker compose run --rm -e DATABASE_URL=postgresql://postgres:example@db:5432/ueba_security web python infrastructure/02_auto_migration_on_startup.py
docker compose up -d --build web
```

Notes & security
- Don't store production secrets in `.env` in the repo.
- Use a secrets manager for production and override environment variables in your deployment platform.
- The compose file maps the DB to host port 5433 to avoid clashing with a host Postgres on 5432; adjust if necessary.

If you want me to push these artifacts to a feature branch and open a PR, tell me the remote name (default `origin`) and the branch name you want (suggestion: `ci/docker-setup`).
