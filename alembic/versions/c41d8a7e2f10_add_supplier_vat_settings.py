"""add supplier VAT settings

Revision ID: c41d8a7e2f10
Revises: 6a0d4fb2c913
Create Date: 2026-11-04 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c41d8a7e2f10"
down_revision: Union[str, Sequence[str], None] = "6a0d4fb2c913"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "suppliers",
        sa.Column(
            "prices_include_vat",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.add_column(
        "suppliers",
        sa.Column("default_vat_rate", sa.Numeric(5, 2), nullable=True),
    )
    op.add_column(
        "supplier_offers",
        sa.Column("vat_rate", sa.Numeric(5, 2), nullable=True),
    )

    # Preserve VAT values already captured in raw import rows.
    op.execute(
        """
        UPDATE supplier_offers
        SET vat_rate = CASE
            WHEN NULLIF(regexp_replace(raw_data->>'vat_rate', '[^0-9.,]', '', 'g'), '') IS NULL
                THEN NULL
            ELSE replace(
                regexp_replace(raw_data->>'vat_rate', '[^0-9.,]', '', 'g'),
                ',',
                '.'
            )::numeric(5, 2)
        END
        WHERE raw_data ? 'vat_rate'
          AND vat_rate IS NULL
        """
    )
    op.alter_column("suppliers", "prices_include_vat", server_default=None)


def downgrade() -> None:
    op.drop_column("supplier_offers", "vat_rate")
    op.drop_column("suppliers", "default_vat_rate")
    op.drop_column("suppliers", "prices_include_vat")
