"""share goods

Revision ID: 2875f4e75e4c
Revises: d34a4152084a
Create Date: 2018-11-23 16:33:25.342809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2875f4e75e4c'
down_revision = 'd34a4152084a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('CorrectNum', sa.Column('CNdate', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('CorrectNum', 'CNdate')
    # ### end Alembic commands ###
