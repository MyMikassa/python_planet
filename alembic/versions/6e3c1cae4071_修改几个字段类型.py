"""修改几个字段类型

Revision ID: 6e3c1cae4071
Revises: a376c5e1f68d
Create Date: 2019-01-06 00:27:02.565645

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6e3c1cae4071'
down_revision = 'a376c5e1f68d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('IndexBanner', 'contentlink',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('IndexBanner', 'contentlink',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
