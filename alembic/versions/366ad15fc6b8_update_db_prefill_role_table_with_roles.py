"""Update DB: Prefill Role Table with roles

Revision ID: 366ad15fc6b8
Revises: 8f1c2b5eabca
Create Date: 2024-08-20 00:04:58.600741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '366ad15fc6b8'
down_revision: Union[str, None] = '8f1c2b5eabca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding new columns (if needed, adjust as required)
    op.add_column('roles', sa.Column('description', sa.String(), nullable=False))
    
    # Insert initial data
    op.execute("""
        INSERT INTO roles (id, name, description) VALUES
        (1, 'admin', 'Administrator with full access'),
        (2, 'mod', 'Moderator with restricted access'),
        (3, 'creator', 'Content creator with specific permissions'),
        (4, 'user', 'Regular user with standard access')
    """)

def downgrade() -> None:
    # Remove the new column (if it was added)
    op.drop_column('roles', 'description')
    
    # Remove the initial data
    op.execute("""
        DELETE FROM roles WHERE id IN (1, 2, 3, 4)
    """)