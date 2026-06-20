"""sistema simulado: tabla simulated_records

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-19
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "simulated_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("invoice_number", sa.String(100), nullable=True),
        sa.Column("invoice_date", sa.String(50), nullable=True),
        sa.Column("provider_name", sa.String(255), nullable=True),
        sa.Column("nit", sa.String(50), nullable=True),
        sa.Column("total", sa.String(50), nullable=True),
        sa.Column("source", sa.String(20), nullable=False, server_default="RPA"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("simulated_records")
