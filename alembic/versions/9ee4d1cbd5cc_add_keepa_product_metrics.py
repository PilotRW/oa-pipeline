"""add keepa product metrics

Revision ID: 9ee4d1cbd5cc
Revises: ae93fab69578
Create Date: 2026-05-23 15:31:50.610105

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9ee4d1cbd5cc"
down_revision: Union[str, Sequence[str], None] = "ae93fab69578"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "keepa_product_metrics",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("asin", sa.String(length=32), nullable=False),
        sa.Column("buy_box_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=True),
        sa.Column("sales_rank", sa.Integer(), nullable=True),
        sa.Column("amazon_in_stock", sa.Boolean(), nullable=True),
        sa.Column("estimated_monthly_sales", sa.Integer(), nullable=True),
        sa.Column(
            "data_status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),
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
        "ix_keepa_product_metrics_asin",
        "keepa_product_metrics",
        ["asin"],
    )

    op.create_index(
        "ix_keepa_product_metrics_data_status",
        "keepa_product_metrics",
        ["data_status"],
    )

    op.create_unique_constraint(
        "uq_keepa_product_metrics_asin",
        "keepa_product_metrics",
        ["asin"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_keepa_product_metrics_asin",
        "keepa_product_metrics",
        type_="unique",
    )

    op.drop_index(
        "ix_keepa_product_metrics_data_status",
        table_name="keepa_product_metrics",
    )

    op.drop_index(
        "ix_keepa_product_metrics_asin",
        table_name="keepa_product_metrics",
    )

    op.drop_table("keepa_product_metrics")
