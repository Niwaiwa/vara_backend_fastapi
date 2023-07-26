"""add user_id and video_id index to video likes table

Revision ID: 2537c7613974
Revises: ef37318f7ce8
Create Date: 2023-07-27 00:16:22.374218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2537c7613974'
down_revision = 'ef37318f7ce8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('idx_video_likes_user_id_video_id', 'video_likes', ['user_id', 'video_id'], unique=True)


def downgrade() -> None:
    op.drop_index('idx_video_likes_user_id_video_id', 'video_likes')
