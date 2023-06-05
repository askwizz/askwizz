"""Create connection table

Revision ID: 1942fe00aee4
Revises: 
Create Date: 2023-06-04 23:46:09.058562

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1942fe00aee4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "connection",
        sa.Column("id", sa.String(50), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("user_id", sa.String(200), nullable=False),
        sa.Column("atlassian_token", sa.String(200), nullable=False),
        sa.Column("atlassian_email", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("connection")
