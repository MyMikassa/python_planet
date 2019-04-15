"""AddFakeSaleValue

Revision ID: 442d560ee00f
Revises: 51e235168984
Create Date: 2019-04-03 18:26:15.723490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '442d560ee00f'
down_revision = '51e235168984'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ProductMonthSaleValue', sa.Column('PMSVfakenum', sa.BIGINT(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ProductMonthSaleValue', 'PMSVfakenum')
    # ### end Alembic commands ###
