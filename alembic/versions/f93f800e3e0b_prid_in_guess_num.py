"""prid in guess num

Revision ID: f93f800e3e0b
Revises: b7c22289a5de
Create Date: 2018-11-26 16:14:18.098406

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f93f800e3e0b'
down_revision = 'b7c22289a5de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('GuessAwardFlow', 'PRid')
    op.add_column('GuessNum', sa.Column('PRid', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('GuessNum', 'PRid')
    op.add_column('GuessAwardFlow', sa.Column('PRid', mysql.VARCHAR(length=64), nullable=True))
    # ### end Alembic commands ###
