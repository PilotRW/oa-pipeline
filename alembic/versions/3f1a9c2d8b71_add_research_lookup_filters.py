"""add research lookup filters

Revision ID: 3f1a9c2d8b71
Revises: 2e4f5b6a7c81
Create Date: 2026-05-27 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers
revision: str = "3f1a9c2d8b71"
down_revision: Union[str, Sequence[str], None] = "2e4f5b6a7c81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "research_rules",
        sa.Column(
            "lookup_excluded_brands",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default="[]",
        ),
    )
    op.add_column(
        "research_rules",
        sa.Column(
            "lookup_excluded_title_keywords",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default="[]",
        ),
    )
    op.add_column(
        "research_rules",
        sa.Column(
            "lookup_min_cost",
            sa.Numeric(10, 2),
            nullable=True,
        ),
    )
    op.add_column(
        "research_rules",
        sa.Column(
            "lookup_max_cost",
            sa.Numeric(10, 2),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("research_rules", "lookup_max_cost")
    op.drop_column("research_rules", "lookup_min_cost")
    op.drop_column("research_rules", "lookup_excluded_title_keywords")
    op.drop_column("research_rules", "lookup_excluded_brands")
