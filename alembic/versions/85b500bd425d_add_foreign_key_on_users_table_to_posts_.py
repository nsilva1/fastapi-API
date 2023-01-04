"""add foreign key on users table to posts table

Revision ID: 85b500bd425d
Revises: 44be2a6a96bc
Create Date: 2023-01-03 16:16:17.072818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85b500bd425d'
down_revision = '44be2a6a96bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('userId', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['userId'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column("posts", "userId")
    pass
