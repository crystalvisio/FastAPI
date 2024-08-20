"""Update DB: Roles Table

Revision ID: 8f1c2b5eabca
Revises: 6ce4cc5d049e
Create Date: 2024-08-19 23:00:10.307263
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8f1c2b5eabca'
down_revision: Union[str, None] = '6ce4cc5d049e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to 'users' table
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default=sa.text('TRUE'), nullable=False))
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=False))

    # Create 'roles' table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False, index=True),
        sa.Column('name', sa.String(), unique=True, index=True)
    )

    # Alter existing columns
    with op.batch_alter_table('posts') as batch_op:
        batch_op.alter_column('published', server_default=sa.text('TRUE'))
    
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('password', type_=sa.String(255))
        
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_user_role', 
        'users', 
        'roles', 
        ['role_id'], 
        ['id']
    )


def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint('fk_user_role', 'users', type_='foreignkey')

    # Drop 'roles' table
    op.drop_table('roles')

    # Remove new columns from 'users' table
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'role_id')

    # Revert existing column alterations
    with op.batch_alter_table('posts') as batch_op:
        batch_op.alter_column('published', server_default=None)

    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('password', type_=sa.String())