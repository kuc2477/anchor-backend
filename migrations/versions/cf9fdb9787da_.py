"""empty message

Revision ID: cf9fdb9787da
Revises: 92fb0db9bfbd
Create Date: 2016-05-01 00:02:39.978838

"""

# revision identifiers, used by Alembic.
revision = 'cf9fdb9787da'
down_revision = '92fb0db9bfbd'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('corpus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('words', sqlalchemy_utils.types.json.JSONType(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('MLP',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('corpus_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['corpus_id'], ['corpus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('MLP')
    op.drop_table('corpus')
    ### end Alembic commands ###
