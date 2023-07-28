"""add tag table and video tag relation table

Revision ID: b36926c14efb
Revises: 2537c7613974
Create Date: 2023-07-28 23:42:21.410038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b36926c14efb'
down_revision = '2537c7613974'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tags',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('slug', sa.String(length=255), nullable=False, unique=True),
    )
    op.create_table(
        'video_tags',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('video_id', sa.UUID(), sa.ForeignKey('videos.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('tag_id', sa.UUID(), sa.ForeignKey('tags.id', ondelete='CASCADE'), nullable=False, index=True),
    )
    op.create_index('idx_video_tags_video_id_tag_id', 'video_tags', ['video_id', 'tag_id'], unique=True)


def downgrade() -> None:
    op.drop_table('video_tags')
    op.drop_table('tags')
