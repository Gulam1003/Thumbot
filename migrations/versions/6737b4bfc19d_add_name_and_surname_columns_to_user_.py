"""Add name and surname columns to User model

Revision ID: 6737b4bfc19d
Revises: 
Create Date: 2023-07-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6737b4bfc19d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=False, server_default='default_name'))
        batch_op.add_column(sa.Column('surname', sa.String(length=50), nullable=False, server_default='default_surname'))

    # Remove the server default after adding the columns
    op.alter_column('user', 'name', server_default=None)
    op.alter_column('user', 'surname', server_default=None)


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('name')
        batch_op.drop_column('surname')
