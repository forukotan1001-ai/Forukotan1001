#!/bin/sh
set -e

echo "Starting entrypoint: waiting for DB (if configured) and running migrations if present"

# optional: wait for DATABASE_URL host if netcat is available and DB host present
if [ -n "$DATABASE_URL" ]; then
  # try to extract host and port; this is a best-effort parse for common URLs
  DB_HOST=$(echo "$DATABASE_URL" | sed -E 's,.*@([^:/]+).*,$\1,') || true
  DB_PORT=$(echo "$DATABASE_URL" | sed -E 's,.*:([0-9]+)/.*,\1,') || true
  if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
    echo "Waiting for DB at $DB_HOST:$DB_PORT"
    # try until pg_isready or nc succeeds
    for i in $(seq 1 30); do
      if command -v pg_isready >/dev/null 2>&1; then
        pg_isready -h "$DB_HOST" -p "$DB_PORT" && break
      elif command -v nc >/dev/null 2>&1; then
        nc -z "$DB_HOST" "$DB_PORT" && break
      fi
      echo "Waiting for DB... ($i)"
      sleep 2
    done
  fi
fi

# Migrations: can be skipped with SKIP_MIGRATIONS=1 or SKIP_MIGRATIONS=true
if [ "${SKIP_MIGRATIONS:-}" = "1" ] || [ "${SKIP_MIGRATIONS:-}" = "true" ]; then
  echo "SKIP_MIGRATIONS is set; skipping migration steps"
else
  # Run migrations in order of preference:
  # 1) Alembic (alembic.ini)
  # 2) repo-specific migration script: infrastructure/02_auto_migration_on_startup.py
  # 3) migrations/setup_database.py
  if [ -f /app/alembic.ini ]; then
    echo "Found alembic.ini: running alembic upgrade head"
    alembic upgrade head
  elif [ -f /app/infrastructure/02_auto_migration_on_startup.py ]; then
    echo "Found infrastructure/02_auto_migration_on_startup.py: running auto-migration script"
    python /app/infrastructure/02_auto_migration_on_startup.py
  elif [ -f /app/migrations/setup_database.py ]; then
    echo "Found migrations/setup_database.py: running it"
    python /app/migrations/setup_database.py
  else
    echo "No migration tool found (alembic or repo migration script). Skipping migrations."
  fi
fi

echo "Starting Uvicorn"
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
