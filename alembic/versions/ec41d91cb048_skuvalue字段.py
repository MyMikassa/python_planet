"""skuvalue字段

Revision ID: ec41d91cb048
Revises: 75d61cf45fad
Create Date: 2018-12-07 20:08:18.321547

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ec41d91cb048'
down_revision = '75d61cf45fad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ProductSkuValue', sa.Column('PRid', sa.String(length=64), nullable=False))
    op.drop_column('ProductSkuValue', 'PCid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ProductSkuValue', sa.Column('PCid', mysql.VARCHAR(collation='utf8_bin', length=64), nullable=False))
    op.drop_column('ProductSkuValue', 'PRid')
    # ### end Alembic commands ###
