"""create initial tables

Revision ID: 00001_create_tables
Revises: 
Create Date: 2025-10-21 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '00001_create_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    
    
    # --- Create ENUM type for user roles ---
    op.execute("CREATE TYPE roleenum AS ENUM ('admin', 'employee')")
    
    # --- Create sectors table ---
    op.create_table(
        'sectors',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(100), unique=True, nullable=False),
        sa.Column('description', sa.String(255)),
    )

    # --- Create users table ---
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(120), unique=True, nullable=False),
        sa.Column('full_name', sa.String(120)),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', role_enum, nullable=False, server_default='employee'),
        sa.Column('sector_id', sa.UUID(as_uuid=True), sa.ForeignKey('sectors.id')),
    )

    # --- Create evaluations table ---
    op.create_table(
        'evaluations',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('evaluator_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
        sa.Column('evaluated_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
        sa.Column('sector_id', sa.UUID(as_uuid=True), sa.ForeignKey('sectors.id', ondelete="CASCADE")),
        sa.Column('score', sa.Integer, nullable=False),
        sa.Column('comments', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Index to prevent self-evaluation
    op.create_check_constraint(
        "no_self_eval",
        "evaluations",
        "evaluator_id != evaluated_id"
    )


def downgrade():
    op.drop_table('evaluations')
    op.drop_table('users')
    op.drop_table('sectors')

    role_enum = sa.Enum('admin', 'employee', name='roleenum', create_type=False)
    role_enum.drop(op.get_bind(), checkfirst=True)
