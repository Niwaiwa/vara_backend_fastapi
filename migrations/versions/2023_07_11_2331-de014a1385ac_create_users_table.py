"""create users table

Revision ID: de014a1385ac
Revises: 
Create Date: 2023-07-11 23:31:38.123518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de014a1385ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False, primary_key=True),
    sa.Column('username', sa.String(length=100), nullable=False, index=True, unique=True),
    sa.Column('email', sa.String(length=255), nullable=False, index=True, unique=True),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('nickname', sa.String(length=100)),
    sa.Column('avatar', sa.String(length=255)),
    sa.Column('header', sa.String(length=255)),
    sa.Column('description', sa.Text()),
    sa.Column('created_time', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
    sa.Column('updated_time', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp(), server_onupdate=sa.func.current_timestamp()),
    sa.Column('locale', sa.String(length=10), nullable=False, server_default='en-US'),
    sa.Column('last_login', sa.DateTime()),
    sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
    sa.Column('is_staff', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
    sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
    )


def downgrade() -> None:
    op.drop_table('users')
