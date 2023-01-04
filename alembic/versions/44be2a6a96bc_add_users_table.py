"""add users table

Revision ID: 44be2a6a96bc
Revises: e7ea9c6dbaa5
Create Date: 2023-01-03 15:50:42.522212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44be2a6a96bc'
down_revision = 'e7ea9c6dbaa5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('createdAt', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
