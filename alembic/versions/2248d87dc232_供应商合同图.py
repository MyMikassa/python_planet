"""供应商合同图

Revision ID: 2248d87dc232
Revises: 2424ef83299b
Create Date: 2018-12-03 17:18:26.655921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2248d87dc232'
down_revision = '2424ef83299b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Supplizer', sa.Column('SUcontract', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Supplizer', 'SUcontract')
    # ### end Alembic commands ###
