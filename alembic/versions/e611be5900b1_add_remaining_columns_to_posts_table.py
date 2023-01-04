"""add remaining columns to posts table

Revision ID: e611be5900b1
Revises: 85b500bd425d
Create Date: 2023-01-03 17:10:31.068924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e611be5900b1'
down_revision = '85b500bd425d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column("posts", sa.Column("createdAt", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "createdAt")
    pass
