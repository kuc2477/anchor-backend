"""empty message

Revision ID: fae9b626cb4d
Revises: f4f023b7c74a
Create Date: 2016-03-16 10:57:14.109950

"""

# revision identifiers, used by Alembic.
revision = 'fae9b626cb4d'
down_revision = 'f4f023b7c74a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('name', sa.Text(), nullable=False, server_default=''))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedule', 'name')
    ### end Alembic commands ###
