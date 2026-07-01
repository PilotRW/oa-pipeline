"""add market snapshots

Revision ID: 6a0d4fb2c913
Revises: 5c8e7f2a9d31
Create Date: 2026-06-30 21:15:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6a0d4fb2c913"
down_revision: Union[str, Sequence[str], None] = "5c8e7f2a9d31"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "market_snapshots",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "amazon_product_match_id",
            sa.BigInteger(),
            sa.ForeignKey("amazon_product_matches.id"),
            nullable=False,
        ),
        sa.Column(
            "queue_id",
            sa.BigInteger(),
            sa.ForeignKey("offer_research_queue.id"),
            nullable=False,
        ),
        sa.Column(
            "supplier_offer_id",
            sa.BigInteger(),
            sa.ForeignKey("supplier_offers.id"),
            nullable=False,
        ),
        sa.Column("asin", sa.String(length=32), nullable=False),
        sa.Column("marketplace", sa.String(length=16), nullable=True),
        sa.Column("current_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("buy_box_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("buy_box_exists", sa.Boolean(), nullable=True),
        sa.Column("sales_rank", sa.Integer(), nullable=True),
        sa.Column("seller_count", sa.Integer(), nullable=True),
        sa.Column("amazon_present", sa.Boolean(), nullable=True),
        sa.Column("fba_fee_estimate", sa.Numeric(10, 2), nullable=True),
        sa.Column("estimated_monthly_sales", sa.Integer(), nullable=True),
        sa.Column("snapshot_source", sa.String(length=50), nullable=True),
        sa.Column(
            "snapshot_status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("error_message", sa.String(length=500), nullable=True),
        sa.Column("raw_data", sa.JSON(), nullable=True),
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
        "ix_market_snapshots_amazon_product_match_id",
        "market_snapshots",
        ["amazon_product_match_id"],
    )
    op.create_index("ix_market_snapshots_queue_id", "market_snapshots", ["queue_id"])
    op.create_index(
        "ix_market_snapshots_supplier_offer_id",
        "market_snapshots",
        ["supplier_offer_id"],
    )
    op.create_index("ix_market_snapshots_asin", "market_snapshots", ["asin"])
    op.create_index(
        "ix_market_snapshots_snapshot_status",
        "market_snapshots",
        ["snapshot_status"],
    )
    op.create_unique_constraint(
        "uq_market_snapshots_amazon_product_match_id",
        "market_snapshots",
        ["amazon_product_match_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_market_snapshots_amazon_product_match_id",
        "market_snapshots",
        type_="unique",
    )
    op.drop_index(
        "ix_market_snapshots_snapshot_status",
        table_name="market_snapshots",
    )
    op.drop_index("ix_market_snapshots_asin", table_name="market_snapshots")
    op.drop_index(
        "ix_market_snapshots_supplier_offer_id",
        table_name="market_snapshots",
    )
    op.drop_index("ix_market_snapshots_queue_id", table_name="market_snapshots")
    op.drop_index(
        "ix_market_snapshots_amazon_product_match_id",
        table_name="market_snapshots",
    )
    op.drop_table("market_snapshots")
