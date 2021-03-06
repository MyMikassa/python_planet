"""'add'

Revision ID: c21685879c11
Revises: 8b86d923c880
Create Date: 2018-11-27 18:27:14.833253

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c21685879c11'
down_revision = '8b86d923c880'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('MagicBox',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('MBid', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('MBid')
    )
    op.add_column('CorrectNum', sa.Column('SKUid', sa.String(length=64), nullable=False))
    op.drop_column('GuessNum', 'PRid')
    op.add_column('User', sa.Column('UScontinuous', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'UScontinuous')
    op.add_column('GuessNum', sa.Column('PRid', mysql.VARCHAR(length=64), nullable=True))
    op.drop_column('CorrectNum', 'SKUid')
    op.drop_table('MagicBox')
    # ### end Alembic commands ###
