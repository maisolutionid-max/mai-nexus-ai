"""Add education teacher assignments table

Revision ID: 20261021_0010
Revises: 20261021_0009
Create Date: 2026-10-21
"""
from alembic import op
import sqlalchemy as sa

revision = '20261021_0010'
down_revision = '20261021_0009'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'education_teacher_assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('school_id', sa.Integer(), nullable=False),
        sa.Column('academic_year_id', sa.Integer(), nullable=False),
        sa.Column('class_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['academic_year_id'], ['education_academic_years.id'], ),
        sa.ForeignKeyConstraint(['class_id'], ['education_classes.id'], ),
        sa.ForeignKeyConstraint(['school_id'], ['education_schools.id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['education_subjects.id'], ),
        sa.ForeignKeyConstraint(['teacher_id'], ['education_teachers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_education_teacher_assignments_id'), 'education_teacher_assignments', ['id'], unique=False)
    op.create_index(op.f('ix_education_teacher_assignments_school_id'), 'education_teacher_assignments', ['school_id'], unique=False)
    op.create_index(op.f('ix_education_teacher_assignments_academic_year_id'), 'education_teacher_assignments', ['academic_year_id'], unique=False)
    op.create_index(op.f('ix_education_teacher_assignments_class_id'), 'education_teacher_assignments', ['class_id'], unique=False)
    op.create_index(op.f('ix_education_teacher_assignments_subject_id'), 'education_teacher_assignments', ['subject_id'], unique=False)
    op.create_index(op.f('ix_education_teacher_assignments_teacher_id'), 'education_teacher_assignments', ['teacher_id'], unique=False)
    op.create_index(op.f('ix_education_teacher_assignments_tenant_id'), 'education_teacher_assignments', ['tenant_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_education_teacher_assignments_tenant_id'), table_name='education_teacher_assignments')
    op.drop_index(op.f('ix_education_teacher_assignments_teacher_id'), table_name='education_teacher_assignments')
    op.drop_index(op.f('ix_education_teacher_assignments_subject_id'), table_name='education_teacher_assignments')
    op.drop_index(op.f('ix_education_teacher_assignments_class_id'), table_name='education_teacher_assignments')
    op.drop_index(op.f('ix_education_teacher_assignments_academic_year_id'), table_name='education_teacher_assignments')
    op.drop_index(op.f('ix_education_teacher_assignments_school_id'), table_name='education_teacher_assignments')
    op.drop_index(op.f('ix_education_teacher_assignments_id'), table_name='education_teacher_assignments')
    op.drop_table('education_teacher_assignments')
