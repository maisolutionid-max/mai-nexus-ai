"""create school users table

Revision ID: 0016
Revises: 0015
Create Date: 2026-10-22 21:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0016"
down_revision = "0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
  op.create_table(
      "school_users",
      sa.Column("id", sa.Integer(), nullable=False),
      sa.Column("school_id", sa.Integer(), nullable=False),
      sa.Column("username", sa.String(length=100), nullable=False),
      sa.Column("email", sa.String(length=255), nullable=False),
      sa.Column("hashed_password", sa.String(length=255), nullable=False),
      sa.Column("full_name", sa.String(length=255), nullable=False),
      sa.Column(
          "role", sa.String(length=50), nullable=False, server_default="student"
      ),
      sa.Column(
          "status", sa.String(length=50), nullable=False, server_default="active"
      ),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
      sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(
      op.f("ix_school_users_id"), "school_users", ["id"], unique=False
  )
  op.create_index(
      op.f("ix_school_users_username"), "school_users", ["username"], unique=True
  )
  op.create_index(
      op.f("ix_school_users_email"), "school_users", ["email"], unique=True
  )


def downgrade() -> None:
  op.drop_index(op.f("ix_school_users_email"), table_name="school_users")
  op.drop_index(op.f("ix_school_users_username"), table_name="school_users")
  op.drop_index(op.f("ix_school_users_id"), table_name="school_users")
  op.drop_table("school_users")
                
