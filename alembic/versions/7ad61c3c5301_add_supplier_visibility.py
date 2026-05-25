"""add supplier visibility

Revision ID: 7ad61c3c5301
Revises: b2f0a7d4c91e
Create Date: 2026-05-25 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "7ad61c3c5301"
down_revision: Union[str, Sequence[str], None] = "b2f0a7d4c91e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "suppliers",
        sa.Column(
            "is_visible",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("suppliers", "is_visible")
