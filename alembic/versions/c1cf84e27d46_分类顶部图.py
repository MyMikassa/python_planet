"""分类顶部图

Revision ID: c1cf84e27d46
Revises: 30ea2e5f626f
Create Date: 2018-12-12 19:37:28.275126

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c1cf84e27d46'
down_revision = '30ea2e5f626f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('OrderRefundApply', 'OMid',
               existing_type=mysql.VARCHAR(collation='utf8_bin', length=64),
                )
    op.add_column('ProductCategory', sa.Column('PCtopPic', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ProductCategory', 'PCtopPic')
    op.alter_column('OrderRefundApply', 'OMid',
               existing_type=mysql.VARCHAR(collation='utf8_bin', length=64),
               nullable=True)
    # ### end Alembic commands ###
