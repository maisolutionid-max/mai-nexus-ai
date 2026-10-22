"""Add education teachers table

Revision ID: 20261021_0008
Revises: 20261021_0007
Create Date: 2026-10-21
"""
from alembic import op
import sqlalchemy as sa

revision = '20261021_0008'
down_revision = '20261021_0007'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'education_teachers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('school_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('nip', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=30), nullable=True),
        sa.Column('specialization', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['school_id'], ['education_schools.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_education_teachers_id'), 'education_teachers', ['id'], unique=False)
    op.create_index(op.f('ix_education_teachers_school_id'), 'education_teachers', ['school_id'], unique=False)
    op.create_index(op.f('ix_education_teachers_tenant_id'), 'education_teachers', ['tenant_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_education_teachers_tenant_id'), table_name='education_teachers')
    op.drop_index(op.f('ix_education_teachers_school_id'), table_name='education_teachers')
    op.drop_index(op.f('ix_education_teachers_id'), table_name='education_teachers')
    op.drop_table('education_teachers')
