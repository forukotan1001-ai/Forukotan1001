import os
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, inspect


def test_migration_contains_idempotent_checks():
    """Static test: ensure the migration contains explicit idempotency checks for
    replay columns and dead_letter_id (helps avoid runtime failures in mixed DB states).
    """
    repo_root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(repo_root, 'alembic', 'versions', '0013_add_webhook_deadletter_replay_fields.py')
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()

    assert "existing_cols = [c['name'] for c in inspector.get_columns('webhook_dead_letters')]" in content
    assert "if 'last_replay_at' not in existing_cols" in content
    assert "if 'dead_letter_id' not in existing_cols" in content
    assert "already present; skipping" in content or "Skipping adding replay columns" in content
