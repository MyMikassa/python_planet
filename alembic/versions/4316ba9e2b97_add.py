"""'add'

Revision ID: 4316ba9e2b97
Revises: 8dce1549b174
Create Date: 2019-01-11 16:46:18.224489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4316ba9e2b97'
down_revision = '8dce1549b174'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ManagerSystemNotes',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('MNid', sa.String(length=64), nullable=False),
    sa.Column('MNcontent', sa.Text(), nullable=True),
    sa.Column('MNstatus', sa.Integer(), nullable=True),
    sa.Column('MNcreateid', sa.String(length=64), nullable=True),
    sa.Column('MNupdateid', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('MNid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ManagerSystemNotes')
    # ### end Alembic commands ###
