
"""Create Education students table.

Revision ID: 20261021_0004
Revises: 20261020_0003
"""

from alembic import op
import sqlalchemy as sa


revision = "20261021_0004"
down_revision = "20261020_0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "education_students",
        sa.Column("id", sa.Integer(), primary_key=True),
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
        sa.Column("student_number", sa.String(50), nullable=False),
        sa.Column("full_name", sa.String(150), nullable=False),
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
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_education_students_tenant_id",
        "education_students",
        ["tenant_id"],
    )
    op.create_index(
        "ix_education_students_school_id",
        "education_students",
        ["school_id"],
    )
    op.create_index(
        "ix_education_students_tenant_school",
        "education_students",
        ["tenant_id", "school_id"],
    )
    op.create_index(
        "ix_education_students_tenant_number",
        "education_students",
        ["tenant_id", "student_number"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        "ix_education_students_tenant_number",
        table_name="education_students",
    )
    op.drop_index(
        "ix_education_students_tenant_school",
        table_name="education_students",
    )
    op.drop_index(
        "ix_education_students_school_id",
        table_name="education_students",
    )
    op.drop_index(
        "ix_education_students_tenant_id",
        table_name="education_students",
    )
    op.drop_table("education_students")
