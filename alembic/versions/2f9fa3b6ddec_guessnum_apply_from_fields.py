"""guessnum_apply_from_fields

Revision ID: 2f9fa3b6ddec
Revises: bca6dfffc4ef
Create Date: 2018-12-28 20:57:01.993228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f9fa3b6ddec'
down_revision = 'bca6dfffc4ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('GuessNumAward', sa.Column('GNAAfrom', sa.Integer(), nullable=True))
    op.add_column('GuessNumAward', sa.Column('SKUstock', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('GuessNumAward', 'SKUstock')
    op.drop_column('GuessNumAward', 'GNAAfrom')
    # ### end Alembic commands ###
