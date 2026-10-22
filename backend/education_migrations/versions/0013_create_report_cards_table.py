"""create report cards table

Revision ID: 0013
Revises: 0012
Create Date: 2026-10-22 10:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
  op.create_table(
      "report_cards",
      sa.Column("id", sa.Integer(), nullable=False),
      sa.Column("school_id", sa.Integer(), nullable=False),
      sa.Column("student_id", sa.Integer(), nullable=False),
      sa.Column("academic_year_id", sa.Integer(), nullable=True),
      sa.Column("term", sa.String(length=50), nullable=False),
      sa.Column("gpa", sa.Float(), nullable=False, server_default="0.0"),
      sa.Column("total_score", sa.Float(), nullable=False, server_default="0.0"),
      sa.Column("rank_in_class", sa.Integer(), nullable=True),
      sa.Column("teacher_notes", sa.Text(), nullable=True),
      sa.Column(
          "status", sa.String(length=50), nullable=False, server_default="Draft"
      ),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(
          ["academic_year_id"], ["academic_years.id"], ondelete="SET NULL"
      ),
      sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
      sa.ForeignKeyConstraint(
          ["student_id"], ["students.id"], ondelete="CASCADE"
      ),
      sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(
      op.f("ix_report_cards_id"), "report_cards", ["id"], unique=False
  )


def downgrade() -> None:
  op.drop_index(op.f("ix_report_cards_id"), table_name="report_cards")
  op.drop_table("report_cards")
    
