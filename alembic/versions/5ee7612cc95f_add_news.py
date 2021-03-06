"""'add_news'

Revision ID: 5ee7612cc95f
Revises: 0b07fd8ee810
Create Date: 2018-11-12 09:46:11.340587

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5ee7612cc95f'
down_revision = '0b07fd8ee810'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('UserAddress', 'AAid',
               existing_type=mysql.VARCHAR(length=8),
               nullable=False)
    op.add_column('UserSearchHistory', sa.Column('USHtype', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserSearchHistory', 'USHtype')
    op.alter_column('UserAddress', 'AAid',
               existing_type=mysql.VARCHAR(length=8),
               nullable=True)
    # ### end Alembic commands ###
