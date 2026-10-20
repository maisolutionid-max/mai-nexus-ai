
"""Create tenants and link education schools.

Revision ID: 20261020_0002
Revises: 20261019_0001
"""

from alembic import op
import sqlalchemy as sa


revision = "20261020_0002"
down_revision = "20261019_0001"
branch_labels = None
depends_on = None


def upgrade():
    # 1. Create tenants table first.
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_tenants_name",
        "tenants",
        ["name"],
    )
    op.create_index(
        "ix_tenants_slug",
        "tenants",
        ["slug"],
        unique=True,
    )

    # 2. SQLite requires batch mode to add a foreign key
    # to an existing table.
    with op.batch_alter_table(
        "education_schools",
        recreate="always",
    ) as batch_op:
        batch_op.add_column(
            sa.Column("tenant_id", sa.Integer(), nullable=True)
        )

        batch_op.create_foreign_key(
            "fk_education_schools_tenant_id",
            "tenants",
            ["tenant_id"],
            ["id"],
            ondelete="RESTRICT",
        )

        batch_op.create_index(
            "ix_education_schools_tenant_id",
            ["tenant_id"],
        )

        batch_op.create_index(
            "ix_education_schools_tenant_active",
            ["tenant_id", "is_active"],
        )


def downgrade():
    # Remove tenant relationship using SQLite batch mode.
    with op.batch_alter_table(
        "education_schools",
        recreate="always",
    ) as batch_op:
        batch_op.drop_index(
            "ix_education_schools_tenant_active",
        )
        batch_op.drop_index(
            "ix_education_schools_tenant_id",
        )
        batch_op.drop_constraint(
            "fk_education_schools_tenant_id",
            type_="foreignkey",
        )
        batch_op.drop_column("tenant_id")

    op.drop_index("ix_tenants_slug", table_name="tenants")
    op.drop_index("ix_tenants_name", table_name="tenants")
    op.drop_table("tenants")
