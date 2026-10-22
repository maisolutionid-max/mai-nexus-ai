"""create grading tables

Revision ID: 0012
Revises: 0011
Create Date: 2026-10-22 09:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
  # Create assessments table
  op.create_table(
      "assessments",
      sa.Column("id", sa.Integer(), nullable=False),
      sa.Column("school_id", sa.Integer(), nullable=False),
      sa.Column("subject_id", sa.Integer(), nullable=False),
      sa.Column("class_id", sa.Integer(), nullable=False),
      sa.Column("teacher_id", sa.Integer(), nullable=True),
      sa.Column("title", sa.String(length=255), nullable=False),
      sa.Column("description", sa.Text(), nullable=True),
      sa.Column("assessment_type", sa.String(length=50), nullable=False),
      sa.Column(
          "max_score", sa.Float(), nullable=False, server_default="100.0"
      ),
      sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
      sa.Column("assessment_date", sa.DateTime(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
      sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
      sa.ForeignKeyConstraint(
          ["subject_id"], ["subjects.id"], ondelete="CASCADE"
      ),
      sa.ForeignKeyConstraint(
          ["teacher_id"], ["teachers.id"], ondelete="SET NULL"
      ),
      sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(
      op.f("ix_assessments_id"), "assessments", ["id"], unique=False
  )

  # Create student_grades table
  op.create_table(
      "student_grades",
      sa.Column("id", sa.Integer(), nullable=False),
      sa.Column("school_id", sa.Integer(), nullable=False),
      sa.Column("assessment_id", sa.Integer(), nullable=False),
      sa.Column("student_id", sa.Integer(), nullable=False),
      sa.Column("score", sa.Float(), nullable=False),
      sa.Column("feedback", sa.Text(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(
          ["assessment_id"], ["assessments.id"], ondelete="CASCADE"
      ),
      sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
      sa.ForeignKeyConstraint(
          ["student_id"], ["students.id"], ondelete="CASCADE"
      ),
      sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(
      op.f("ix_student_grades_id"), "student_grades", ["id"], unique=False
  )


def downgrade() -> None:
  op.drop_index(op.f("ix_student_grades_id"), table_name="student_grades")
  op.drop_table("student_grades")
  op.drop_index(op.f("ix_assessments_id"), table_name="assessments")
  op.drop_table("assessments")
                
