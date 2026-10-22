"""Add education classes table

Revision ID: 20261021_0006
Revises: 20261021_0005
Create Date: 2026-10-21
"""
from alembic import op
import sqlalchemy as sa

revision = '20261021_0006'
down_revision = '20261021_0005'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'education_classes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('school_id', sa.Integer(), nullable=False),
        sa.Column('academic_year_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('grade_level', sa.String(length=20), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['academic_year_id'], ['education_academic_years.id'], ),
        sa.ForeignKeyConstraint(['school_id'], ['education_schools.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_education_classes_id'), 'education_classes', ['id'], unique=False)
    op.create_index(op.f('ix_education_classes_school_id'), 'education_classes', ['school_id'], unique=False)
    op.create_index(op.f('ix_education_classes_academic_year_id'), 'education_classes', ['academic_year_id'], unique=False)
    op.create_index(op.f('ix_education_classes_tenant_id'), 'education_classes', ['tenant_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_education_classes_tenant_id'), table_name='education_classes')
    op.drop_index(op.f('ix_education_classes_academic_year_id'), table_name='education_classes')
    op.drop_index(op.f('ix_education_classes_school_id'), table_name='education_classes')
    op.drop_index(op.f('ix_education_classes_id'), table_name='education_classes')
    op.drop_table('education_classes')
                  
