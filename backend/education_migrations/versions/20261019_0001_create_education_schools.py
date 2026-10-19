
"""Create education_schools table."""

from alembic import op
import sqlalchemy as sa


revision = "20261019_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "education_schools",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("npsn", sa.String(length=20), nullable=True),
        sa.Column(
            "school_level",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "school_type",
            sa.String(length=50),
            nullable=False,
            server_default="general",
        ),
        sa.Column("address", sa.String(length=500), nullable=True),
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
        sa.UniqueConstraint("npsn", name="uq_education_schools_npsn"),
    )
    op.create_index(
        "ix_education_schools_npsn",
        "education_schools",
        ["npsn"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        "ix_education_schools_npsn",
        table_name="education_schools",
    )
    op.drop_table("education_schools")
