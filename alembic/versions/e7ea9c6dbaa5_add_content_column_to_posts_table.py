"""add content column to posts table

Revision ID: e7ea9c6dbaa5
Revises: d0892436238d
Create Date: 2023-01-03 15:42:40.434028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7ea9c6dbaa5'
down_revision = 'd0892436238d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
