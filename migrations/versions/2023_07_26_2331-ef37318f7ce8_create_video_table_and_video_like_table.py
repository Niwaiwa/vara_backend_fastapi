"""create video table and video like table

Revision ID: ef37318f7ce8
Revises: 485130a23687
Create Date: 2023-07-26 23:31:30.949461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef37318f7ce8'
down_revision = '485130a23687'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'videos',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('video_file', sa.String(length=255), nullable=True),
        sa.Column('video_url', sa.String(length=255), nullable=True),
        sa.Column('rating', sa.CHAR(length=2), nullable=False),
        sa.Column('views_count', sa.Integer(), nullable=False, default=0),
        sa.Column('likes_count', sa.Integer(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_table(
        'video_likes',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('video_id', sa.UUID(), sa.ForeignKey('videos.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('video_likes')
    op.drop_table('videos')
