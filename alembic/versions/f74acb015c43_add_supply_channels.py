"""add supply channels

Revision ID: f74acb015c43
Revises: e63fab904b32
Create Date: 2026-11-05 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "f74acb015c43"
down_revision: Union[str, Sequence[str], None] = "e63fab904b32"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "supplier_offers",
        sa.Column(
            "supply_channel",
            sa.Text(),
            server_default="stock",
            nullable=False,
        ),
    )
    op.add_column(
        "supplier_offers",
        sa.Column("lead_time_min_days", sa.Integer(), nullable=True),
    )
    op.add_column(
        "supplier_offers",
        sa.Column("lead_time_max_days", sa.Integer(), nullable=True),
    )
    op.create_index(
        "ix_supplier_offers_supply_channel",
        "supplier_offers",
        ["supply_channel"],
        unique=False,
    )
    op.add_column(
        "ingestion_runs",
        sa.Column(
            "supply_channel_assignments",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("ingestion_runs", "supply_channel_assignments")
    op.drop_index(
        "ix_supplier_offers_supply_channel",
        table_name="supplier_offers",
    )
    op.drop_column("supplier_offers", "lead_time_max_days")
    op.drop_column("supplier_offers", "lead_time_min_days")
    op.drop_column("supplier_offers", "supply_channel")
