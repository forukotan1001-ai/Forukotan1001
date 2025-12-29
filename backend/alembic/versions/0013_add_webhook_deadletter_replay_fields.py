"""add last_replay_at and replay_count to webhook dead letters; add dead_letter_id to attempts

Revision ID: 0013_add_webhook_deadletter_replay_fields
Revises: 0012_add_webhook_deadletter_processed
Create Date: 2025-12-26 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0013_add_webhook_deadletter_replay_fields'
down_revision = '0012_add_webhook_deadletter_processed'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'webhook_dead_letters' in inspector.get_table_names():
        existing_cols = [c['name'] for c in inspector.get_columns('webhook_dead_letters')]
        if 'last_replay_at' not in existing_cols:
            op.add_column('webhook_dead_letters', sa.Column('last_replay_at', sa.DateTime(timezone=True), nullable=True))
        else:
            print('Column last_replay_at already present; skipping')

        if 'replay_count' not in existing_cols:
            op.add_column('webhook_dead_letters', sa.Column('replay_count', sa.Integer(), nullable=False, server_default=sa.text('0')))
        else:
            print('Column replay_count already present; skipping')

        if 'auto_replay' not in existing_cols:
            op.add_column('webhook_dead_letters', sa.Column('auto_replay', sa.Boolean(), nullable=False, server_default=sa.text('0')))
        else:
            print('Column auto_replay already present; skipping')
    else:
        print('Skipping adding replay columns: webhook_dead_letters table not present in DB')

    # Add dead_letter_id to attempts so we can associate replays with the originating dead letter
    if 'webhook_attempts' in inspector.get_table_names():
        existing_cols = [c['name'] for c in inspector.get_columns('webhook_attempts')]
        if 'dead_letter_id' not in existing_cols:
            op.add_column('webhook_attempts', sa.Column('dead_letter_id', sa.Integer(), nullable=True))
            op.create_foreign_key('fk_webhook_attempts_dead_letter_id', 'webhook_attempts', 'webhook_dead_letters', ['dead_letter_id'], ['id'], ondelete='SET NULL')
            op.create_index(op.f('idx_webhook_attempts_dead_letter_id'), 'webhook_attempts', ['dead_letter_id'])
        else:
            print('Column dead_letter_id already present; skipping')
    else:
        print('Skipping adding dead_letter_id: webhook_attempts table not present in DB')


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    try:
        if 'webhook_attempts' in inspector.get_table_names():
            cols = [c['name'] for c in inspector.get_columns('webhook_attempts')]
            if 'dead_letter_id' in cols:
                try:
                    op.drop_index(op.f('idx_webhook_attempts_dead_letter_id'), table_name='webhook_attempts')
                except Exception:
                    print('Index idx_webhook_attempts_dead_letter_id not present or could not be dropped')
                try:
                    op.drop_constraint('fk_webhook_attempts_dead_letter_id', 'webhook_attempts', type_='foreignkey')
                except Exception:
                    print('Foreign key fk_webhook_attempts_dead_letter_id not present or could not be dropped')
                op.drop_column('webhook_attempts', 'dead_letter_id')
    except Exception as e:
        print('Skipping dropping dead_letter_id: %s' % e)

    try:
        if 'webhook_dead_letters' in inspector.get_table_names():
            cols = [c['name'] for c in inspector.get_columns('webhook_dead_letters')]
            if 'replay_count' in cols:
                op.drop_column('webhook_dead_letters', 'replay_count')
            if 'auto_replay' in cols:
                op.drop_column('webhook_dead_letters', 'auto_replay')
            if 'last_replay_at' in cols:
                op.drop_column('webhook_dead_letters', 'last_replay_at')
    except Exception as e:
        print('Skipping dropping replay columns: %s' % e)
