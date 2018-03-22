"""empty message

Revision ID: f9c390d9b050
Revises: bc58312c47a3
Create Date: 2018-03-20 14:50:54.312766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f9c390d9b050'
down_revision = 'bc58312c47a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statusTable',
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('ID', sa.String(length=10), nullable=True),
    sa.Column('changeTime', sa.DateTime(), nullable=True),
    sa.Column('col1', sa.String(length=50), nullable=True),
    sa.Column('col2', sa.String(length=50), nullable=True),
    sa.Column('col3', sa.String(length=50), nullable=True),
    sa.Column('col4', sa.String(length=50), nullable=True),
    sa.Column('col5', sa.String(length=50), nullable=True),
    sa.Column('col6', sa.String(length=50), nullable=True),
    sa.Column('col7', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['ID'], ['devicesTable.ID'], ),
    sa.PrimaryKeyConstraint('num')
    )
    op.drop_table('status1001Table')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status1001Table',
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
    sa.ForeignKeyConstraint(['ID'], [u'devicesTable.ID'], name=u'status1001table_ibfk_1'),
    sa.PrimaryKeyConstraint('num'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('statusTable')
    # ### end Alembic commands ###