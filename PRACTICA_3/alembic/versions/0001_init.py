from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "providers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("nit", sa.String(50), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("address", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_providers_nit", "providers", ["nit"], unique=True)

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("invoice_number", sa.String(100), nullable=True),
        sa.Column("invoice_date", sa.String(50), nullable=True),
        sa.Column("provider_name", sa.String(255), nullable=True),
        sa.Column("nit", sa.String(50), nullable=True),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=True),
        sa.Column("taxes", sa.Numeric(12, 2), nullable=True),
        sa.Column("total", sa.Numeric(12, 2), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDIENTE"),
        sa.Column("file_path", sa.String(500), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id"), nullable=True),
        sa.Column("uploaded_by_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "processing_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("document_name", sa.String(255), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("invoice_id", sa.Integer(), sa.ForeignKey("invoices.id"), nullable=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("processing_logs")
    op.drop_table("invoices")
    op.drop_index("ix_providers_nit", table_name="providers")
    op.drop_table("providers")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
