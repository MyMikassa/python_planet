"""new_filelds_add_mainpic

Revision ID: b626301225a8
Revises: d99f2386d171
Create Date: 2018-12-05 16:29:56.046446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b626301225a8'
down_revision = 'd99f2386d171'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('News', sa.Column('NEisrecommend', sa.Boolean(), nullable=True))
    op.add_column('News', sa.Column('NEmainpic', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('News', 'NEmainpic')
    op.drop_column('News', 'NEisrecommend')
    # ### end Alembic commands ###
