"""'add'

Revision ID: 1e2c8f0e9731
Revises: ff06d923722c
Create Date: 2019-04-11 18:04:41.750509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e2c8f0e9731'
down_revision = 'ff06d923722c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Carts', sa.Column('Contentid', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Carts', 'Contentid')
    # ### end Alembic commands ###