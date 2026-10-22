"""Add education attendances table

Revision ID: 20261021_0011
Revises: 20261021_0010
Create Date: 2026-10-21
"""
from alembic import op
import sqlalchemy as sa

revision = '20261021_0011'
down_revision = '20261021_0010'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'education_attendances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('school_id', sa.Integer(), nullable=False),
        sa.Column('class_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('notes', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['class_id'], ['education_classes.id'], ),
        sa.ForeignKeyConstraint(['school_id'], ['education_schools.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['education_students.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_education_attendances_id'), 'education_attendances', ['id'], unique=False)
    op.create_index(op.f('ix_education_attendances_school_id'), 'education_attendances', ['school_id'], unique=False)
    op.create_index(op.f('ix_education_attendances_class_id'), 'education_attendances', ['class_id'], unique=False)
    op.create_index(op.f('ix_education_attendances_student_id'), 'education_attendances', ['student_id'], unique=False)
    op.create_index(op.f('ix_education_attendances_date'), 'education_attendances', ['date'], unique=False)
    op.create_index(op.f('ix_education_attendances_tenant_id'), 'education_attendances', ['tenant_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_education_attendances_tenant_id'), table_name='education_attendances')
    op.drop_index(op.f('ix_education_attendances_date'), table_name='education_attendances')
    op.drop_index(op.f('ix_education_attendances_student_id'), table_name='education_attendances')
    op.drop_index(op.f('ix_education_attendances_class_id'), table_name='education_attendances')
    op.drop_index(op.f('ix_education_attendances_school_id'), table_name='education_attendances')
    op.drop_index(op.f('ix_education_attendances_id'), table_name='education_attendances')
    op.drop_table('education_attendances')
