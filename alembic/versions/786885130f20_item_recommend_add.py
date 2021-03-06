"""'item_recommend_add'

Revision ID: 786885130f20
Revises: 3aa068e88568
Create Date: 2018-11-14 19:48:23.768118

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '786885130f20'
down_revision = '3aa068e88568'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('CouponUser', sa.Column('UCalreadyUse', sa.Boolean(), nullable=True))
    op.drop_column('CouponUser', 'UCuserStatus')
    op.add_column('Items', sa.Column('ITrecommend', sa.Boolean(), nullable=True))
    op.add_column('NewsImage', sa.Column('NIthumbnail', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('NewsImage', 'NIthumbnail')
    op.drop_column('Items', 'ITrecommend')
    op.add_column('CouponUser', sa.Column('UCuserStatus', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('CouponUser', 'UCalreadyUse')
    # ### end Alembic commands ###
