"""001_baseline

Revision ID: 001_baseline
Revises:
Create Date: 2026-01-01 00:00:00.000000

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '001_baseline'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Baseline creates no business tables yet
    pass


def downgrade() -> None:
    pass
