"""Create search_history table

Revision ID: c24bfdd468e8
Revises: 1942fe00aee4
Create Date: 2023-07-09 17:18:57.648717

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c24bfdd468e8"
down_revision = "1942fe00aee4"
table_name = "search_history"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.String(50), primary_key=True),
        sa.Column("user_id", sa.String(200), nullable=False),
        sa.Column("search", sa.String(1024), nullable=False),
    )


def downgrade() -> None:
    op.drop_table(table_name)
