"""字段名

Revision ID: b69247d8f473
Revises: b247fd61d7c7
Create Date: 2018-11-02 18:00:12.920149

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b69247d8f473'
down_revision = 'b247fd61d7c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('OrderPart', 'PRid',
               existing_type=mysql.VARCHAR(collation='utf8_bin', length=64),
               nullable=False)
    op.add_column('OrderPay', sa.Column('OPaymarks', sa.String(length=255), nullable=True))
    op.drop_column('OrderPay', 'OPmarks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('OrderPay', sa.Column('OPmarks', mysql.VARCHAR(collation='utf8_bin', length=255), nullable=True))
    op.drop_column('OrderPay', 'OPaymarks')
    op.alter_column('OrderPart', 'PRid',
               existing_type=mysql.VARCHAR(collation='utf8_bin', length=64),
               nullable=True)
    # ### end Alembic commands ###
