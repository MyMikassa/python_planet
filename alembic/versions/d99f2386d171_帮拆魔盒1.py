"""帮拆魔盒1

Revision ID: d99f2386d171
Revises: 76a5aee8c546
Create Date: 2018-12-05 15:00:05.032037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd99f2386d171'
down_revision = '76a5aee8c546'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('MagicBoxJoin', sa.Column('MBJcurrentPrice', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('MagicBoxJoin', 'MBJcurrentPrice')
    # ### end Alembic commands ###
