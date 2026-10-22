"""create announcements table

Revision ID: 0015
Revises: 0014
Create Date: 2026-10-22 21:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
  op.create_table(
      "announcements",
      sa.Column("id", sa.Integer(), nullable=False),
      sa.Column("school_id", sa.Integer(), nullable=False),
      sa.Column("teacher_id", sa.Integer(), nullable=True),
      sa.Column("title", sa.String(length=255), nullable=False),
      sa.Column("content", sa.Text(), nullable=False),
      sa.Column(
          "target_role", sa.String(length=50), nullable=False, server_default="all"
      ),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
      sa.ForeignKeyConstraint(
          ["teacher_id"], ["teachers.id"], ondelete="SET NULL"
      ),
      sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(
      op.f("ix_announcements_id"), "announcements", ["id"], unique=False
  )


def downgrade() -> None:
  op.drop_index(op.f("ix_announcements_id"), table_name="announcements")
  op.drop_table("announcements")

