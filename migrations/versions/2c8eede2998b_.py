"""empty message

Revision ID: 2c8eede2998b
Revises: 3a845b6b0d9e
Create Date: 2016-05-28 21:21:00.502813

"""

# revision identifiers, used by Alembic.
revision = '2c8eede2998b'
down_revision = '3a845b6b0d9e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('type', sa.String(), nullable=False, server_default='url'))
    op.drop_column('schedule', 'news_type')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('news_type', sa.VARCHAR(), server_default=sa.text("'url'::character varying"), autoincrement=False, nullable=False))
    op.drop_column('schedule', 'type')
    ### end Alembic commands ###
