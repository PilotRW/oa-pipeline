"""add supplier offer price tiers

Revision ID: e63fab904b32
Revises: d52e9b8f3a21
Create Date: 2026-11-04 15:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "e63fab904b32"
down_revision: Union[str, Sequence[str], None] = "d52e9b8f3a21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "supplier_offers",
        sa.Column(
            "price_tiers",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("supplier_offers", "price_tiers")
