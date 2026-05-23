"""add offer research queue

Revision ID: f0272990c254
Revises: 47d371ba918e
Create Date: 2026-05-22 20:25:56.365782

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f0272990c254"
down_revision: Union[str, Sequence[str], None] = "47d371ba918e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "offer_research_queue",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "supplier_offer_id",
            sa.Integer(),
            sa.ForeignKey("supplier_offers.id"),
            nullable=False,
        ),

        sa.Column(
            "supplier_id",
            sa.Integer(),
            sa.ForeignKey("suppliers.id"),
            nullable=False,
        ),

        sa.Column(
            "ean",
            sa.String(length=32),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="new",
        ),

        sa.Column(
            "priority_score",
            sa.Numeric(10, 2),
            nullable=True,
        ),

        sa.Column(
            "rejection_reason",
            sa.Text(),
            nullable=True,
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
        "ix_offer_research_queue_ean",
        "offer_research_queue",
        ["ean"],
    )

    op.create_index(
        "ix_offer_research_queue_status",
        "offer_research_queue",
        ["status"],
    )

    op.create_unique_constraint(
        "uq_offer_research_queue_supplier_offer_id",
        "offer_research_queue",
        ["supplier_offer_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_offer_research_queue_supplier_offer_id",
        "offer_research_queue",
        type_="unique",
    )

    op.drop_index(
        "ix_offer_research_queue_status",
        table_name="offer_research_queue",
    )

    op.drop_index(
        "ix_offer_research_queue_ean",
        table_name="offer_research_queue",
    )

    op.drop_table("offer_research_queue")