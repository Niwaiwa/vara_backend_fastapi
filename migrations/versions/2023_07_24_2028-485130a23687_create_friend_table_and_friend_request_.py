"""create friend table and friend request table

Revision ID: 485130a23687
Revises: d8442ed477a1
Create Date: 2023-07-24 20:28:46.688623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '485130a23687'
down_revision = 'd8442ed477a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'friends',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('friend_user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True), 
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_table(
        'friend_requests',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('from_user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('to_user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('friend')
    op.drop_table('friend_request')
