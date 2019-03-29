"""'add'

Revision ID: c60527e297dd
Revises: efb958e7178c
Create Date: 2019-03-26 20:33:53.391804

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c60527e297dd'
down_revision = 'efb958e7178c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ProductUrl',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('PUid', sa.String(length=64), nullable=False),
    sa.Column('PUurl', sa.Text(), nullable=False),
    sa.Column('PUdir', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('PUid')
    )
    op.alter_column('CompanyMessage', 'CMreadnum',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.add_column('Products', sa.Column('PRcode', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Products', 'PRcode')
    op.alter_column('CompanyMessage', 'CMreadnum',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_table('ProductUrl')
    # ### end Alembic commands ###