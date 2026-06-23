"""add supplier price tracking

Revision ID: 5c8e7f2a9d31
Revises: 4b7d3a9c6e12
Create Date: 2026-06-23 15:15:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5c8e7f2a9d31"
down_revision: Union[str, Sequence[str], None] = "4b7d3a9c6e12"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("suppliers", sa.Column("price_etag", sa.Text(), nullable=True))
    op.add_column(
        "suppliers",
        sa.Column("price_last_modified", sa.Text(), nullable=True),
    )
    op.add_column(
        "suppliers",
        sa.Column("price_content_length", sa.BigInteger(), nullable=True),
    )
    op.add_column(
        "suppliers",
        sa.Column("price_file_hash", sa.Text(), nullable=True),
    )
    op.add_column(
        "suppliers",
        sa.Column("price_data_hash", sa.Text(), nullable=True),
    )
    op.add_column(
        "suppliers",
        sa.Column("price_last_filename", sa.Text(), nullable=True),
    )
    op.add_column(
        "suppliers",
        sa.Column("price_update_status", sa.Text(), nullable=True),
    )
    op.add_column(
        "suppliers",
        sa.Column(
            "price_last_checked_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )
    op.add_column(
        "suppliers",
        sa.Column(
            "price_last_downloaded_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )
    op.add_column(
        "suppliers",
        sa.Column(
            "price_last_changed_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("suppliers", "price_last_changed_at")
    op.drop_column("suppliers", "price_last_downloaded_at")
    op.drop_column("suppliers", "price_last_checked_at")
    op.drop_column("suppliers", "price_update_status")
    op.drop_column("suppliers", "price_last_filename")
    op.drop_column("suppliers", "price_data_hash")
    op.drop_column("suppliers", "price_file_hash")
    op.drop_column("suppliers", "price_content_length")
    op.drop_column("suppliers", "price_last_modified")
    op.drop_column("suppliers", "price_etag")
