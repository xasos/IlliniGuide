"""empty message

Revision ID: fa97886baa62
Revises: f5ab31d06461
Create Date: 2016-08-11 21:04:41.947335

"""

# revision identifiers, used by Alembic.
revision = 'fa97886baa62'
down_revision = 'f5ab31d06461'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_reviews', sa.Column('grade', sa.Text(), nullable=False))
    op.add_column('user_reviews', sa.Column('groupwork', sa.Numeric(), nullable=False))
    op.add_column('user_reviews', sa.Column('hoursperweek', sa.Integer(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_reviews', 'hoursperweek')
    op.drop_column('user_reviews', 'groupwork')
    op.drop_column('user_reviews', 'grade')
    ### end Alembic commands ###
