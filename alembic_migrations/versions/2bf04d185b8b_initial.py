"""initial

Revision ID: 2bf04d185b8b
Revises: 
Create Date: 2025-01-28 19:34:06.311754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bf04d185b8b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('username', sa.String(255), primary_key=True),
        sa.Column('server_nick', sa.String(255), nullable=True),
        sa.Column('mention', sa.String(255), nullable=True),
    )

    op.create_table(
        'words',
        sa.Column('word', sa.String(255), primary_key=True),
        sa.Column('count', sa.Integer, default=0, nullable=True)
    )
    
    op.create_table(
        'user_words',
        sa.Column('username', sa.String(255), sa.ForeignKey('users.username'), primary_key=True),
        sa.Column('word', sa.String(255), sa.ForeignKey('words.word'), primary_key=True),
        sa.Column('count', sa.Integer, default=0, nullable=True)
    )

    op.create_table(
        'channels',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=True)
    )

    op.create_table(
        'channel_words',
        sa.Column('channel_id', sa.Integer, sa.ForeignKey('channels.id'), primary_key=True),
        sa.Column('word', sa.String(255), sa.ForeignKey('words.word'), primary_key=True),
        sa.Column('count', sa.Integer, default=0, nullable=True)
    )

    op.create_table(
        'favour_table',
        sa.Column('username', sa.String(255), sa.ForeignKey('users.username'), primary_key=True),
        sa.Column('favour', sa.Integer, default=0, nullable=True)
    )

    op.create_table(
        'fortunes_table',
        sa.Column('username', sa.String(255), sa.ForeignKey('users.username'), primary_key=True),
        sa.Column('allowed', sa.Boolean, default=True, nullable=True)
    )

    op.create_table(
        'mention_bot_table',
        sa.Column('username', sa.String(255), sa.ForeignKey('users.username'), primary_key=True),
        sa.Column('mention_count', sa.Integer, default=0, nullable=True)
    )

    op.create_table(
        'vocabulary_table',
        sa.Column('vocabulary', sa.String(255), primary_key=True),
        sa.Column('username', sa.String(255), sa.ForeignKey('users.username'))
    )

    op.create_table(
        'nuke_table',
        sa.Column('username', sa.String(255), sa.ForeignKey('users.username'), primary_key=True),
        sa.Column('nuke_count', sa.Integer, default=0, nullable=True),
        sa.Column('defuse_count', sa.Integer, default=0, nullable=True),
        sa.Column('allowed', sa.Boolean, default=True, nullable=True)
    )

    op.create_table(
        'highscores',
        sa.Column('username', sa.String(255), sa.ForeignKey('users.username'), primary_key=True),
        sa.Column('best_score_russian', sa.Integer, default=0, nullable=True),
        sa.Column('curr_score_russian', sa.Integer, default=0, nullable=True),
        sa.Column('best_score_hardcore', sa.Integer, default=0, nullable=True),
        sa.Column('curr_score_hardcore', sa.Integer, default=0, nullable=True),
        sa.Column('best_score_glock', sa.Integer, default=0, nullable=True),
        sa.Column('curr_score_glock', sa.Integer, default=0, nullable=True),
    )

    op.create_table(
        'global_variables',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('state', sa.Integer, default=0, nullable=True),
        sa.Column('intensity', sa.Integer, default=1, nullable=True),
        sa.Column('message_count', sa.Integer, default=0, nullable=True),
        sa.Column('timestamp', sa.DateTime, nullable=True),
        sa.Column('death_roll', sa.Integer, default=100),
    )


def downgrade():
    op.drop_table('global_variables')
    op.drop_table('high_scores')
    op.drop_table('nuke_table')
    op.drop_table('vocabulary_table')
    op.drop_table('mention_bot_table')
    op.drop_table('fortune_table')
    op.drop_table('favour_table')
    op.drop_table('channel_words')
    op.drop_table('channels')
    op.drop_table('user_words')
    op.drop_table('words')
    op.drop_table('users')
