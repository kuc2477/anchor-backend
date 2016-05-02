"""empty message

Revision ID: a748217173c3
Revises: c12f49bb1296
Create Date: 2016-05-02 23:24:52.404726

"""

# revision identifiers, used by Alembic.
revision = 'a748217173c3'
down_revision = 'c12f49bb1296'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'SVM', ['user_id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'SVM', type_='unique')
    ### end Alembic commands ###
