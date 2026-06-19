"""add amazon presence checks

Revision ID: 8c2d9a1f0b34
Revises: 3f1a9c2d8b71
Create Date: 2026-06-15 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8c2d9a1f0b34"
down_revision: Union[str, Sequence[str], None] = "3f1a9c2d8b71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "amazon_presence_checks",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "amazon_product_match_id",
            sa.BigInteger(),
            sa.ForeignKey("amazon_product_matches.id"),
            nullable=False,
        ),
        sa.Column(
            "supplier_offer_id",
            sa.BigInteger(),
            sa.ForeignKey("supplier_offers.id"),
            nullable=False,
        ),
        sa.Column("asin", sa.String(length=32), nullable=False),
        sa.Column("marketplace", sa.String(length=8), nullable=True),
        sa.Column("amazon_present", sa.Boolean(), nullable=True),
        sa.Column(
            "presence_status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("data_source", sa.String(length=50), nullable=True),
        sa.Column("checked_at", sa.DateTime(), nullable=True),
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
        "ix_amazon_presence_checks_amazon_product_match_id",
        "amazon_presence_checks",
        ["amazon_product_match_id"],
        unique=True,
    )
    op.create_index(
        "ix_amazon_presence_checks_supplier_offer_id",
        "amazon_presence_checks",
        ["supplier_offer_id"],
    )
    op.create_index(
        "ix_amazon_presence_checks_asin",
        "amazon_presence_checks",
        ["asin"],
    )
    op.create_index(
        "ix_amazon_presence_checks_presence_status",
        "amazon_presence_checks",
        ["presence_status"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_amazon_presence_checks_presence_status",
        table_name="amazon_presence_checks",
    )
    op.drop_index(
        "ix_amazon_presence_checks_asin",
        table_name="amazon_presence_checks",
    )
    op.drop_index(
        "ix_amazon_presence_checks_supplier_offer_id",
        table_name="amazon_presence_checks",
    )
    op.drop_index(
        "ix_amazon_presence_checks_amazon_product_match_id",
        table_name="amazon_presence_checks",
    )
    op.drop_table("amazon_presence_checks")
