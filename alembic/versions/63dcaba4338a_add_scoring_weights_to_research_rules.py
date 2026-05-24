"""add scoring weights to research rules

Revision ID: 63dcaba4338a
Revises: d517a82a04ca
Create Date: 2026-05-23 19:54:22.537956
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "63dcaba4338a"
down_revision: Union[str, Sequence[str], None] = "d517a82a04ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "research_rules",
        sa.Column(
            "score_stock_high",
            sa.Integer(),
            nullable=False,
            server_default="30",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_stock_medium",
            sa.Integer(),
            nullable=False,
            server_default="20",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_stock_low",
            sa.Integer(),
            nullable=False,
            server_default="10",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_stock_very_low",
            sa.Integer(),
            nullable=False,
            server_default="-20",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_cost_preferred",
            sa.Integer(),
            nullable=False,
            server_default="30",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_cost_medium",
            sa.Integer(),
            nullable=False,
            server_default="15",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_cost_high",
            sa.Integer(),
            nullable=False,
            server_default="-10",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_cost_low",
            sa.Integer(),
            nullable=False,
            server_default="-20",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_brand_present",
            sa.Integer(),
            nullable=False,
            server_default="15",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_title_present",
            sa.Integer(),
            nullable=False,
            server_default="15",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "score_ean_present",
            sa.Integer(),
            nullable=False,
            server_default="10",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "research_rules",
        "score_ean_present",
    )

    op.drop_column(
        "research_rules",
        "score_title_present",
    )

    op.drop_column(
        "research_rules",
        "score_brand_present",
    )

    op.drop_column(
        "research_rules",
        "score_cost_low",
    )

    op.drop_column(
        "research_rules",
        "score_cost_high",
    )

    op.drop_column(
        "research_rules",
        "score_cost_medium",
    )

    op.drop_column(
        "research_rules",
        "score_cost_preferred",
    )

    op.drop_column(
        "research_rules",
        "score_stock_very_low",
    )

    op.drop_column(
        "research_rules",
        "score_stock_low",
    )

    op.drop_column(
        "research_rules",
        "score_stock_medium",
    )

    op.drop_column(
        "research_rules",
        "score_stock_high",
    )