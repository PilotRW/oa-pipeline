"""add pipeline settings and research rules

Revision ID: d517a82a04ca
Revises: ef6936e4aeba
Create Date: 2026-05-23 19:22:52.678098

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d517a82a04ca"
down_revision: Union[str, Sequence[str], None] = "ef6936e4aeba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "pipeline_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("use_real_keepa", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("default_batch_size", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("default_marketplace", sa.String(length=16), nullable=False, server_default="DE"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "research_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("min_priority_score", sa.Numeric(10, 2), nullable=False, server_default="80"),
        sa.Column("min_stock", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("low_stock_threshold", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("medium_stock_threshold", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("high_stock_threshold", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("preferred_cost_min", sa.Numeric(10, 2), nullable=False, server_default="20"),
        sa.Column("preferred_cost_max", sa.Numeric(10, 2), nullable=False, server_default="300"),
        sa.Column("medium_cost_max", sa.Numeric(10, 2), nullable=False, server_default="1000"),
        sa.Column("min_cost", sa.Numeric(10, 2), nullable=False, server_default="5"),
        sa.Column("min_roi_percent", sa.Numeric(10, 2), nullable=False, server_default="20"),
        sa.Column("min_profit", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("max_sales_rank", sa.Integer(), nullable=True),
        sa.Column("min_monthly_sales", sa.Integer(), nullable=True),
        sa.Column("exclude_amazon_in_stock", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.execute(
        """
        INSERT INTO pipeline_settings (
            id,
            use_real_keepa,
            default_batch_size,
            default_marketplace
        )
        VALUES (
            1,
            false,
            20,
            'DE'
        )
        """
    )

    op.execute(
        """
        INSERT INTO research_rules (
            id,
            min_priority_score,
            min_stock,
            low_stock_threshold,
            medium_stock_threshold,
            high_stock_threshold,
            preferred_cost_min,
            preferred_cost_max,
            medium_cost_max,
            min_cost,
            min_roi_percent,
            min_profit,
            exclude_amazon_in_stock
        )
        VALUES (
            1,
            80,
            1,
            1,
            3,
            20,
            20,
            300,
            1000,
            5,
            20,
            0,
            false
        )
        """
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("research_rules")
    op.drop_table("pipeline_settings")