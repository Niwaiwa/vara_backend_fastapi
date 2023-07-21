"""create following table and add column to user table

Revision ID: d8442ed477a1
Revises: de014a1385ac
Create Date: 2023-07-21 21:23:10.437282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8442ed477a1'
down_revision = 'de014a1385ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'followings',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('following_user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('followings')
