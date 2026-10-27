
"""Add role to education tenant users.

Revision ID: add_edu_tenant_role
Revises: REPLACE_WITH_CURRENT_REVISION
"""

from alembic import op
import sqlalchemy as sa


revision = "add_edu_tenant_role"
down_revision = "REPLACE_WITH_CURRENT_REVISION"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "education_tenant_users",
        sa.Column(
            "role",
            sa.String(length=30),
            nullable=False,
            server_default="teacher",
        ),
    )

    op.create_index(
        "ix_education_tenant_users_role",
        "education_tenant_users",
        ["role"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        "ix_education_tenant_users_role",
        table_name="education_tenant_users",
    )

    op.drop_column(
        "education_tenant_users",
        "role",
    )
