"""领奖

Revision ID: 4845e31088d0
Revises: 3541b44d30e9
Create Date: 2018-11-26 11:09:56.842247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4845e31088d0'
down_revision = '3541b44d30e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guess_award_flow',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('GAFid', sa.String(length=64), nullable=False),
    sa.Column('GNid', sa.String(length=64), nullable=False),
    sa.Column('GAFstatus', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('GAFid'),
    sa.UniqueConstraint('GNid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('guess_award_flow')
    # ### end Alembic commands ###
