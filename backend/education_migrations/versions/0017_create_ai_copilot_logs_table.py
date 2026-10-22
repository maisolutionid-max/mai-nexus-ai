"""create ai copilot logs table

Revision ID: 0017
Revises: 0016
Create Date: 2026-10-22 22:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
  op.create_table(
      "ai_copilot_logs",
      sa.Column("id", sa.Integer(), nullable=False),
      sa.Column("school_id", sa.Integer(), nullable=False),
      sa.Column("teacher_id", sa.Integer(), nullable=True),
      sa.Column("student_id", sa.Integer(), nullable=True),
      sa.Column("feature_type", sa.String(length=100), nullable=False),
      sa.Column("prompt_input", sa.Text(), nullable=False),
      sa.Column("ai_response", sa.Text(), nullable=False),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
      sa.ForeignKeyConstraint(
          ["teacher_id"], ["teachers.id"], ondelete="SET NULL"
      ),
      sa.ForeignKeyConstraint(
          ["student_id"], ["students.id"], ondelete="CASCADE"
      ),
      sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(
      op.f("ix_ai_copilot_logs_id"), "ai_copilot_logs", ["id"], unique=False
  )


def downgrade() -> None:
  op.drop_index(op.f("ix_ai_copilot_logs_id"), table_name="ai_copilot_logs")
  op.drop_table("ai_copilot_logs")
    
