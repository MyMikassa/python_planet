"""字段索引

Revision ID: 7844e2262761
Revises: 002a5c0b049e
Create Date: 2018-11-09 09:18:47.665654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7844e2262761'
down_revision = '002a5c0b049e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_OrderPay_OPayno'), 'OrderPay', ['OPayno'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_OrderPay_OPayno'), table_name='OrderPay')
    # ### end Alembic commands ###
