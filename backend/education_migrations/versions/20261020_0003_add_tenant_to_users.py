
"""Add tenant ownership to users.

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
    with op.batch_alter_table(
        "users",
        recreate="always",
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "tenant_id",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_foreign_key(
            "fk_users_tenant_id",
            "tenants",
            ["tenant_id"],
            ["id"],
            ondelete="RESTRICT",
        )

        batch_op.create_index(
            "ix_users_tenant_id",
            ["tenant_id"],
        )


def downgrade():
    with op.batch_alter_table(
        "users",
        recreate="always",
    ) as batch_op:
        batch_op.drop_index("ix_users_tenant_id")

        batch_op.drop_constraint(
            "fk_users_tenant_id",
            type_="foreignkey",
        )

        batch_op.drop_column("tenant_id")
