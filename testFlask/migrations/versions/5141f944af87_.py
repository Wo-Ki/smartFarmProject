"""empty message

Revision ID: 5141f944af87
Revises: b71e2b24fb9c
Create Date: 2018-03-20 14:42:49.642155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5141f944af87'
down_revision = 'b71e2b24fb9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devicesTable',
    sa.Column('ID', sa.String(length=10), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('changeTime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('greenHouseImages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imgData', sa.BLOB(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('logTable',
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('log', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('num')
    )
    op.create_table('alertTable',
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('ID', sa.String(length=10), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ID'], ['devicesTable.ID'], ),
    sa.PrimaryKeyConstraint('num')
    )
    op.create_table('data1001Table',
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('ID', sa.String(length=10), nullable=True),
    sa.Column('temIn', sa.String(length=10), nullable=True),
    sa.Column('humIn', sa.String(length=10), nullable=True),
    sa.Column('temOut', sa.String(length=10), nullable=True),
    sa.Column('humOut', sa.String(length=10), nullable=True),
    sa.Column('temSoil1', sa.String(length=10), nullable=True),
    sa.Column('humSoil1', sa.String(length=10), nullable=True),
    sa.Column('temSoil2', sa.String(length=10), nullable=True),
    sa.Column('humSoil2', sa.String(length=10), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ID'], ['devicesTable.ID'], ),
    sa.PrimaryKeyConstraint('num')
    )
    op.create_table('notificationTable',
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('SID', sa.String(length=10), nullable=True),
    sa.Column('TID', sa.Text(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['SID'], ['devicesTable.ID'], ),
    sa.PrimaryKeyConstraint('num')
    )
    op.create_table('statusChenTable',
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('ID', sa.String(length=10), nullable=True),
    sa.Column('changeTime', sa.DateTime(), nullable=True),
    sa.Column('water1', sa.String(length=20), nullable=True),
    sa.Column('water2', sa.String(length=20), nullable=True),
    sa.Column('windCtrl1', sa.String(length=20), nullable=True),
    sa.Column('windCtrl2', sa.String(length=20), nullable=True),
    sa.Column('doorCtrl', sa.String(length=20), nullable=True),
    sa.Column('lightCtrl', sa.String(length=20), nullable=True),
    sa.Column('temCtrl', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['ID'], ['devicesTable.ID'], ),
    sa.PrimaryKeyConstraint('num')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statusChenTable')
    op.drop_table('notificationTable')
    op.drop_table('data1001Table')
    op.drop_table('alertTable')
    op.drop_table('logTable')
    op.drop_table('greenHouseImages')
    op.drop_table('devicesTable')
    # ### end Alembic commands ###
