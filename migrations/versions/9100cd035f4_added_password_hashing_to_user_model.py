"""added password hashing to user model

Revision ID: 9100cd035f4
Revises: 3a693f41d5dc
Create Date: 2015-06-04 11:18:37.044917

"""

# revision identifiers, used by Alembic.
revision = '9100cd035f4'
down_revision = '3a693f41d5dc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password_hash')
    ### end Alembic commands ###
