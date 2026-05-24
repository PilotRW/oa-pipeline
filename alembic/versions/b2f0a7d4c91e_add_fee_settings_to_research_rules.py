"""add fee settings to research rules

Revision ID: b2f0a7d4c91e
Revises: 63dcaba4338a
Create Date: 2026-05-24 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "b2f0a7d4c91e"
down_revision: Union[str, Sequence[str], None] = "63dcaba4338a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "research_rules",
        sa.Column(
            "referral_fee_percent",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="15",
        ),
    )

    op.add_column(
        "research_rules",
        sa.Column(
            "fulfillment_fee_fixed",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="5",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "research_rules",
        "fulfillment_fee_fixed",
    )

    op.drop_column(
        "research_rules",
        "referral_fee_percent",
    )
