"""modify_evaluation

Revision ID: 9d2d9a2f9bb3
Revises: 25802cb07269
Create Date: 2018-11-20 21:56:28.141941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d2d9a2f9bb3'
down_revision = '25802cb07269'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('OrderEvaluation', sa.Column('PRid', sa.String(length=64), nullable=False))
    op.add_column('OrderEvaluation', sa.Column('SKUattriteDetail', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('OrderEvaluation', 'SKUattriteDetail')
    op.drop_column('OrderEvaluation', 'PRid')
    # ### end Alembic commands ###
