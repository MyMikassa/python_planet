"""供应商最低比

Revision ID: 8dce1549b174
Revises: f18aa539f759
Create Date: 2019-01-11 16:25:35.395142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8dce1549b174'
down_revision = 'f18aa539f759'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Supplizer', sa.Column('SUbaseRate', sa.DECIMAL(scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Supplizer', 'SUbaseRate')
    # ### end Alembic commands ###
