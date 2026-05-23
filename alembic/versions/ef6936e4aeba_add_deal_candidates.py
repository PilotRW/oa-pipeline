"""add deal candidates

Revision ID: ef6936e4aeba
Revises: 9ee4d1cbd5cc
Create Date: 2026-05-23 15:48:01.704635

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ef6936e4aeba"
down_revision: Union[str, Sequence[str], None] = "9ee4d1cbd5cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "deal_candidates",

        sa.Column(
            "id",
            sa.BigInteger(),
            primary_key=True,
        ),

        sa.Column(
            "supplier_offer_id",
            sa.BigInteger(),
            sa.ForeignKey("supplier_offers.id"),
            nullable=False,
        ),

        sa.Column(
            "asin",
            sa.String(length=32),
            nullable=False,
        ),

        sa.Column(
            "supplier_cost",
            sa.Numeric(10, 2),
            nullable=False,
        ),

        sa.Column(
            "amazon_price",
            sa.Numeric(10, 2),
            nullable=True,
        ),

        sa.Column(
            "estimated_fees",
            sa.Numeric(10, 2),
            nullable=True,
        ),

        sa.Column(
            "estimated_profit",
            sa.Numeric(10, 2),
            nullable=True,
        ),

        sa.Column(
            "roi_percent",
            sa.Numeric(10, 2),
            nullable=True,
        ),

        sa.Column(
            "sales_rank",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "estimated_monthly_sales",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_deal_candidates_asin",
        "deal_candidates",
        ["asin"],
    )

    op.create_index(
        "ix_deal_candidates_status",
        "deal_candidates",
        ["status"],
    )

    op.create_index(
        "ix_deal_candidates_roi",
        "deal_candidates",
        ["roi_percent"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_deal_candidates_roi",
        table_name="deal_candidates",
    )

    op.drop_index(
        "ix_deal_candidates_status",
        table_name="deal_candidates",
    )

    op.drop_index(
        "ix_deal_candidates_asin",
        table_name="deal_candidates",
    )

    op.drop_table("deal_candidates")