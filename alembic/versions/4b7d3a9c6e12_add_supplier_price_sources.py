"""add supplier price sources

Revision ID: 4b7d3a9c6e12
Revises: 8c2d9a1f0b34
Create Date: 2026-06-23 14:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "4b7d3a9c6e12"
down_revision: Union[str, Sequence[str], None] = "8c2d9a1f0b34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "suppliers",
        sa.Column("price_url", sa.Text(), nullable=True),
    )
    op.add_column(
        "suppliers",
        sa.Column(
            "import_filter_profile",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("suppliers", "import_filter_profile")
    op.drop_column("suppliers", "price_url")
