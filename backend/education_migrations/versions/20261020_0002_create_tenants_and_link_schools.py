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
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
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
        sa.UniqueConstraint("slug", name="uq_tenants_slug"),
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

    op.add_column(
        "education_schools",
        sa.Column("tenant_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_education_schools_tenant_id",
        "education_schools",
        "tenants",
        ["tenant_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.create_index(
        "ix_education_schools_tenant_id",
        "education_schools",
        ["tenant_id"],
    )

    op.create_index(
        "ix_education_schools_tenant_active",
        "education_schools",
        ["tenant_id", "is_active"],
    )


def downgrade():
    op.drop_index(
        "ix_education_schools_tenant_active",
        table_name="education_schools",
    )
    op.drop_index(
        "ix_education_schools_tenant_id",
        table_name="education_schools",
    )

    op.drop_constraint(
        "fk_education_schools_tenant_id",
        "education_schools",
        type_="foreignkey",
    )

    op.drop_column("education_schools", "tenant_id")

    op.drop_index("ix_tenants_slug", table_name="tenants")
    op.drop_index("ix_tenants_name", table_name="tenants")
    op.drop_table("tenants")
          
