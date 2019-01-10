"""'add'

Revision ID: 659a62e03c5f
Revises: 3f1a1dd891f1
Create Date: 2019-01-10 13:51:29.074508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '659a62e03c5f'
down_revision = '3f1a1dd891f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('SettlenmentApply',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('SSAid', sa.String(length=64), nullable=False),
    sa.Column('SUid', sa.String(length=64), nullable=True),
    sa.Column('SSid', sa.String(length=64), nullable=True),
    sa.Column('SSAabo', sa.Text(), nullable=True),
    sa.Column('SSArejectReason', sa.Text(), nullable=True),
    sa.Column('SSAstatus', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('SSAid')
    )
    op.create_table('SupplizerAccount',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('SAid', sa.String(length=64), nullable=False),
    sa.Column('SPid', sa.String(length=64), nullable=True),
    sa.Column('SAbankName', sa.Text(), nullable=True),
    sa.Column('SAbankDetail', sa.Text(), nullable=True),
    sa.Column('SAcardNo', sa.String(length=32), nullable=True),
    sa.Column('SAcardName', sa.Text(), nullable=True),
    sa.Column('SACompanyName', sa.Text(), nullable=True),
    sa.Column('SAICIDcode', sa.Text(), nullable=True),
    sa.Column('SAaddress', sa.Text(), nullable=True),
    sa.Column('SAbankAccount', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('SAid')
    )
    op.create_table('SupplizerSettlement',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('SSid', sa.String(length=64), nullable=False),
    sa.Column('SUid', sa.String(length=64), nullable=True),
    sa.Column('SSstatus', sa.Integer(), nullable=True),
    sa.Column('SSdealTime', sa.DateTime(), nullable=True),
    sa.Column('SSdealamount', sa.DECIMAL(precision=28, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('SSid')
    )
    op.add_column('Supplizer', sa.Column('SUbusinessLicense', sa.Text(), nullable=True))
    op.add_column('Supplizer', sa.Column('SUemail', sa.String(length=256), nullable=True))
    op.add_column('Supplizer', sa.Column('SUlegalPerson', sa.Text(), nullable=True))
    op.add_column('Supplizer', sa.Column('SUlegalPersonIDcardBack', sa.Text(), nullable=True))
    op.add_column('Supplizer', sa.Column('SUlegalPersonIDcardFront', sa.Text(), nullable=True))
    op.add_column('Supplizer', sa.Column('SUmainCategory', sa.Text(), nullable=True))
    op.add_column('Supplizer', sa.Column('SUregisteredFund', sa.String(length=255), nullable=True))
    op.add_column('Supplizer', sa.Column('SUregisteredTime', sa.DateTime(), nullable=True))
    op.add_column('UserWallet', sa.Column('UWexpect', sa.DECIMAL(precision=28, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserWallet', 'UWexpect')
    op.drop_column('Supplizer', 'SUregisteredTime')
    op.drop_column('Supplizer', 'SUregisteredFund')
    op.drop_column('Supplizer', 'SUmainCategory')
    op.drop_column('Supplizer', 'SUlegalPersonIDcardFront')
    op.drop_column('Supplizer', 'SUlegalPersonIDcardBack')
    op.drop_column('Supplizer', 'SUlegalPerson')
    op.drop_column('Supplizer', 'SUemail')
    op.drop_column('Supplizer', 'SUbusinessLicense')
    op.drop_table('SupplizerSettlement')
    op.drop_table('SupplizerAccount')
    op.drop_table('SettlenmentApply')
    # ### end Alembic commands ###
