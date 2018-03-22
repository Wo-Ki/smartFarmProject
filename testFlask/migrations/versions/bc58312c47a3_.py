"""empty message

Revision ID: bc58312c47a3
Revises: 5141f944af87
Create Date: 2018-03-20 14:43:35.369698

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bc58312c47a3'
down_revision = '5141f944af87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status1001Table',
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
    op.drop_table('statusChenTable')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statusChenTable',
    sa.Column('num', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('ID', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('changeTime', mysql.DATETIME(), nullable=True),
    sa.Column('water1', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('water2', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('windCtrl1', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('windCtrl2', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('doorCtrl', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('lightCtrl', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('temCtrl', mysql.VARCHAR(length=20), nullable=True),
    sa.ForeignKeyConstraint(['ID'], [u'devicesTable.ID'], name=u'statuschentable_ibfk_1'),
    sa.PrimaryKeyConstraint('num'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('status1001Table')
    # ### end Alembic commands ###