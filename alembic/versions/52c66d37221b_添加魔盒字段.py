"""添加魔盒字段

Revision ID: 52c66d37221b
Revises: f1c503ed1cf7
Create Date: 2018-12-06 15:07:33.992726

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '52c66d37221b'
down_revision = 'f1c503ed1cf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('FreshManFirstProduct',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('FMFPid', sa.String(length=64), nullable=False),
    sa.Column('PRid', sa.String(length=64), nullable=False),
    sa.Column('PRmainpic', sa.String(length=255), nullable=False),
    sa.Column('PRtitle', sa.String(length=255), nullable=False),
    sa.Column('PBid', sa.String(length=64), nullable=False),
    sa.Column('PRdescription', sa.Text(), nullable=True),
    sa.Column('PRattribute', sa.Text(), nullable=True),
    sa.Column('PRfeight', sa.Float(), nullable=True),
    sa.Column('PRprice', sa.Float(), nullable=False),
    sa.Column('FMFAid', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('FMFPid')
    )
    op.create_table('FreshManFirstSku',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('FMFSid', sa.String(length=64), nullable=False),
    sa.Column('FMFPid', sa.String(length=64), nullable=False),
    sa.Column('SKUid', sa.String(length=64), nullable=False),
    sa.Column('SKUpic', sa.String(length=255), nullable=False),
    sa.Column('SKUprice', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('FMFSid')
    )
    op.drop_column('FreshManFirstApply', 'PRid')
    op.add_column('MagicBoxApply', sa.Column('PBid', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('MagicBoxApply', 'PBid')
    op.add_column('FreshManFirstApply', sa.Column('PRid', mysql.VARCHAR(length=64), nullable=False))
    op.drop_table('FreshManFirstSku')
    op.drop_table('FreshManFirstProduct')
    # ### end Alembic commands ###
