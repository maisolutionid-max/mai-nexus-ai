"""Create Education user-to-tenant assignments.

Revision ID: 20261020_0003
Revises: 20261020_0002
"""

from alembic import op
import sqlalchemy as sa


revision = "20261020_0003"
down_revision = "20261020_0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "education_tenant_users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_education_tenant_users_tenant_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "user_id",
            name="uq_education_tenant_users_user_id",
        ),
    )

    op.create_index(
        "ix_education_tenant_users_tenant_id",
        "education_tenant_users",
        ["tenant_id"],
    )


def downgrade():
    op.drop_index(
        "ix_education_tenant_users_tenant_id",
        table_name="education_tenant_users",
    )
    op.drop_table("education_tenant_users")
          
