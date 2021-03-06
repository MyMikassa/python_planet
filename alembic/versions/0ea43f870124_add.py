"""add

Revision ID: 0ea43f870124
Revises: 694e0bd72d59
Create Date: 2018-11-07 16:02:39.343437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ea43f870124'
down_revision = '694e0bd72d59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('OrderRefundApply', sa.Column('ORAproductStatus', sa.Integer(), nullable=True))
    op.add_column('OrderRefundApply', sa.Column('ORAsn', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('OrderRefundApply', 'ORAsn')
    op.drop_column('OrderRefundApply', 'ORAproductStatus')
    # ### end Alembic commands ###
