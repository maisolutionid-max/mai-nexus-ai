
"""Create education academic years.

Revision ID: 20261021_0005
Revises: REPLACE_WITH_ACTUAL_0004_REVISION_ID
Create Date: 2026-10-21
"""

from alembic import op
import sqlalchemy as sa


revision = "20261021_0005"
down_revision = "REPLACE_WITH_ACTUAL_0004_REVISION_ID"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "education_academic_years",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "tenant_id",
            sa.Integer(),
            sa.ForeignKey("tenants.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "school_id",
            sa.Integer(),
            sa.ForeignKey("education_schools.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
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
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "school_id",
            "name",
            name="uq_education_academic_year_school_name",
        ),
        sa.CheckConstraint(
            "end_date > start_date",
            name="ck_education_academic_year_dates",
        ),
    )

    op.create_index(
        "ix_education_academic_years_tenant_id",
        "education_academic_years",
        ["tenant_id"],
    )
    op.create_index(
        "ix_education_academic_years_school_id",
        "education_academic_years",
        ["school_id"],
    )
    op.create_index(
        "ix_education_academic_year_tenant_school",
        "education_academic_years",
        ["tenant_id", "school_id"],
    )


def downgrade():
    op.drop_index(
        "ix_education_academic_year_tenant_school",
        table_name="education_academic_years",
    )
    op.drop_index(
        "ix_education_academic_years_school_id",
        table_name="education_academic_years",
    )
    op.drop_index(
        "ix_education_academic_years_tenant_id",
        table_name="education_academic_years",
    )
    op.drop_table("education_academic_years")
