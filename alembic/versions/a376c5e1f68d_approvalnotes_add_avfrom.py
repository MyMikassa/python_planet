"""ApprovalNotes_add_AVfrom

Revision ID: a376c5e1f68d
Revises: b21c819f6453
Create Date: 2019-01-03 11:01:09.309728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a376c5e1f68d'
down_revision = 'b21c819f6453'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ApprovalNotes', sa.Column('ANfrom', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ApprovalNotes', 'ANfrom')
    # ### end Alembic commands ###
