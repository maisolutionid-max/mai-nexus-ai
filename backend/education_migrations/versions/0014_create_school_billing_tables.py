"""create school billing tables

Revision ID: 0014
Revises: 0013
Create Date: 2026-10-22 10:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
  # Create school_bills table
  op.create_table(
      "school_bills",
      sa.Column("id", sa.Integer(), nullable=False),
      sa.Column("school_id", sa.Integer(), nullable=False),
      sa.Column("student_id", sa.Integer(), nullable=False),
      sa.Column("title", sa.String(length=255), nullable=False),
      sa.Column("description", sa.Text(), nullable=True),
      sa.Column("amount", sa.Float(), nullable=False, server_default="0.0"),
      sa.Column("due_date", sa.DateTime(), nullable=True),
      sa.Column(
          "status",
          sa.String(length=50),
          nullable=False,
          server_default="Unpaid",
      ),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
      sa.ForeignKeyConstraint(
          ["student_id"], ["students.id"], ondelete="CASCADE"
      ),
      sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(
      op.f("ix_school_bills_id"), "school_bills", ["id"], unique=False
  )

  # Create bill_payments table
  op.create_table(
      "bill_payments",
      sa.Column("id", sa.Integer(), nullable=False),
      sa.Column("school_id", sa.Integer(), nullable=False),
      sa.Column("bill_id", sa.Integer(), nullable=False),
      sa.Column("amount_paid", sa.Float(), nullable=False, server_default="0.0"),
      sa.Column("payment_date", sa.DateTime(), nullable=False),
      sa.Column("payment_method", sa.String(length=50), nullable=True),
      sa.Column("reference_number", sa.String(length=100), nullable=True),
      sa.Column("notes", sa.Text(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(
          ["bill_id"], ["school_bills.id"], ondelete="CASCADE"
      ),
      sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
      sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(
      op.f("ix_bill_payments_id"), "bill_payments", ["id"], unique=False
  )


def downgrade() -> None:
  op.drop_index(op.f("ix_bill_payments_id"), table_name="bill_payments")
  op.drop_table("bill_payments")
  op.drop_index(op.f("ix_school_bills_id"), table_name="school_bills")
  op.drop_table("school_bills")
