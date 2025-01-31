"""anticheat

Revision ID: ccdcc68d54cf
Revises: 2bf04d185b8b
Create Date: 2025-01-31 20:11:13.958313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccdcc68d54cf'
down_revision: Union[str, None] = '2bf04d185b8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('user_words', sa.Column('cheat_timestamp', sa.DateTime, nullable=True))
    op.add_column('user_words', sa.Column('cheat_count', sa.Integer, default=1))


def downgrade():
    op.drop_column('user_words', 'cheat_timestamp')
    op.drop_column('user_words', 'cheat_count')
