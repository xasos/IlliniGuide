"""empty message

Revision ID: 8b752b2eb39d
Revises: 1e6827a57c66
Create Date: 2016-07-02 22:01:06.191248

"""

# revision identifiers, used by Alembic.
revision = '8b752b2eb39d'
down_revision = '1e6827a57c66'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_reviews', 'easiness')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_reviews', sa.Column('easiness', sa.NUMERIC(), autoincrement=False, nullable=False))
    ### end Alembic commands ###