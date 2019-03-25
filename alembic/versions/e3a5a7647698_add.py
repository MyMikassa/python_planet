"""'add'

Revision ID: e3a5a7647698
Revises: 90334a8dc89e
Create Date: 2019-02-24 23:36:16.508321

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e3a5a7647698'
down_revision = '90334a8dc89e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('GuessNum', 'PRid',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.alter_column('GuessNum', 'Price',
               existing_type=mysql.FLOAT(),
               nullable=True)
    op.alter_column('GuessNum', 'SKUid',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('GuessNum', 'SKUid',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.alter_column('GuessNum', 'Price',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.alter_column('GuessNum', 'PRid',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###