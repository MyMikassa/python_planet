"""'add_NEid'

Revision ID: c0eb8458afd1
Revises: 82138cb190a8
Create Date: 2018-11-12 19:34:29.823969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0eb8458afd1'
down_revision = '82138cb190a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('NewsImage', sa.Column('NEid', sa.String(length=64), nullable=False))
    op.add_column('NewsVideo', sa.Column('NEid', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('NewsVideo', 'NEid')
    op.drop_column('NewsImage', 'NEid')
    # ### end Alembic commands ###
