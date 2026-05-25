"""add supplier rule profiles

Revision ID: 2e4f5b6a7c81
Revises: 7ad61c3c5301
Create Date: 2026-05-25 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "2e4f5b6a7c81"
down_revision: Union[str, Sequence[str], None] = "7ad61c3c5301"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "research_rules",
        sa.Column(
            "supplier_id",
            sa.Integer(),
            sa.ForeignKey("suppliers.id"),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_research_rules_supplier_id_unique",
        "research_rules",
        ["supplier_id"],
        unique=True,
        postgresql_where=sa.text("supplier_id IS NOT NULL"),
    )
    op.execute(
        """
        SELECT setval(
            pg_get_serial_sequence('research_rules', 'id'),
            COALESCE((SELECT MAX(id) FROM research_rules), 1)
        )
        """
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_research_rules_supplier_id_unique",
        table_name="research_rules",
    )
    op.drop_column("research_rules", "supplier_id")
