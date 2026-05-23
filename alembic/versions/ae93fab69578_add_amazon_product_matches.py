"""add amazon product matches

Revision ID: ae93fab69578
Revises: f0272990c254
Create Date: 2026-05-22 21:07:10.246287

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ae93fab69578"
down_revision: Union[str, Sequence[str], None] = "f0272990c254"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "amazon_product_matches",

        sa.Column(
            "id",
            sa.BigInteger(),
            primary_key=True,
        ),

        sa.Column(
            "queue_id",
            sa.Integer(),
            sa.ForeignKey("offer_research_queue.id"),
            nullable=False,
        ),

        sa.Column(
            "supplier_offer_id",
            sa.BigInteger(),
            sa.ForeignKey("supplier_offers.id"),
            nullable=False,
        ),

        sa.Column(
            "ean",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "asin",
            sa.String(length=32),
            nullable=True,
        ),

        sa.Column(
            "match_status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),

        sa.Column(
            "match_confidence",
            sa.Numeric(5, 2),
            nullable=True,
        ),

        sa.Column(
            "amazon_title",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "amazon_brand",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "matched_at",
            sa.DateTime(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_amazon_product_matches_ean",
        "amazon_product_matches",
        ["ean"],
    )

    op.create_index(
        "ix_amazon_product_matches_asin",
        "amazon_product_matches",
        ["asin"],
    )

    op.create_index(
        "ix_amazon_product_matches_status",
        "amazon_product_matches",
        ["match_status"],
    )

    op.create_unique_constraint(
        "uq_amazon_product_matches_queue_id",
        "amazon_product_matches",
        ["queue_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_amazon_product_matches_queue_id",
        "amazon_product_matches",
        type_="unique",
    )

    op.drop_index(
        "ix_amazon_product_matches_status",
        table_name="amazon_product_matches",
    )

    op.drop_index(
        "ix_amazon_product_matches_asin",
        table_name="amazon_product_matches",
    )

    op.drop_index(
        "ix_amazon_product_matches_ean",
        table_name="amazon_product_matches",
    )

    op.drop_table("amazon_product_matches")