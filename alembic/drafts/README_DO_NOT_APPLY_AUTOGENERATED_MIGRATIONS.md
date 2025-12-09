DO NOT APPLY THESE AUTO-GENERATED MIGRATIONS
===========================================

This folder is a storage area for auto-generated Alembic revisions that should
not be applied to the database as-is because they contain destructive or
incomplete operations (DROP TABLE / DROP INDEX) that were produced by a
misconfigured autogenerate run.

Files moved here (for review / manual editing):
- 0bb41fb5ccd6_initial_models.py.bak  (original broken autogen)
- 6ec1fc7bfa87_initial_models_regen.py (regenerated autogen - still contains destructive drops)

Recommended workflow:
1. Keep the current manual baseline revision `006bd7033a3f_initial_models.py`
   as the canonical initial Alembic revision (it is intentionally empty).
2. Do NOT run `alembic upgrade head` until you have a reviewed migration.
3. To produce a safe migration, re-run `alembic revision --autogenerate` in a
   controlled environment where `alembic.env` imports the same declarative
   metadata as your application (this repo's `app.models` package). Inspect
   the generated file and convert DROP operations into CREATEs, or split the
   revision into multiple smaller revisions with explicit FK ordering.
4. When ready, move the reviewed revision(s) into `alembic/versions/` and
   commit. Then CI/production can safely run `alembic upgrade head`.

If you need me to inspect or repair the generated migrations, say so and I
will open them and propose a safe edit (non-destructive create-ordering).

This file was created automatically by the migration-recovery assistant.
