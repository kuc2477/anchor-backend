"""empty message

Revision ID: cc54a6f29fca
Revises: 9d465ca8d6e2
Create Date: 2016-01-29 10:18:04.521000

"""

# revision identifiers, used by Alembic.
revision = 'cc54a6f29fca'
down_revision = '9d465ca8d6e2'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

from app.users.models import User


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sqlalchemy_utils.types.choice.ChoiceType(User.ROLES), 
                                    nullable=False, default=User.USER))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    ### end Alembic commands ###