"""empty message

Revision ID: f5ab31d06461
Revises: 8b752b2eb39d
Create Date: 2016-07-05 17:40:54.016612

"""

# revision identifiers, used by Alembic.
revision = 'f5ab31d06461'
down_revision = '8b752b2eb39d'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('SSO', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('SSOProvider', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'SSOProvider')
    op.drop_column('user', 'SSO')
    ### end Alembic commands ###
