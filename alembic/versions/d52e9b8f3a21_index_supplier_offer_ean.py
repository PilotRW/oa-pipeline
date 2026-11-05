"""index supplier offer EAN

Revision ID: d52e9b8f3a21
Revises: c41d8a7e2f10
Create Date: 2026-11-04 12:20:00.000000

"""

from typing import Sequence, Union

from alembic import op


revision: str = "d52e9b8f3a21"
down_revision: Union[str, Sequence[str], None] = "c41d8a7e2f10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_supplier_offers_ean",
        "supplier_offers",
        ["ean"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_supplier_offers_ean", table_name="supplier_offers")
