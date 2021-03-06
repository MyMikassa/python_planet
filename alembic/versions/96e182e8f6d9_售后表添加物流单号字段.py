"""售后表添加物流单号字段


Revision ID: 96e182e8f6d9
Revises: 6c3bc5e0c5b9
Create Date: 2018-11-21 17:55:05.703570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96e182e8f6d9'
down_revision = '6c3bc5e0c5b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('OrderRefund', sa.Column('ORlogisticsn', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_OrderRefund_ORAid'), 'OrderRefund', ['ORAid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_OrderRefund_ORAid'), table_name='OrderRefund')
    op.drop_column('OrderRefund', 'ORlogisticsn')
    # ### end Alembic commands ###
