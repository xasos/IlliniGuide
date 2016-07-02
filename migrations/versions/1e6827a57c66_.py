"""empty message

Revision ID: 1e6827a57c66
Revises: b9ce31c2c771
Create Date: 2016-07-02 20:33:58.579315

"""

# revision identifiers, used by Alembic.
revision = '1e6827a57c66'
down_revision = 'b9ce31c2c771'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('professor', sa.Text(), nullable=False),
    sa.Column('classname', sa.Text(), nullable=False),
    sa.Column('comments', sa.Text(), nullable=False),
    sa.Column('easiness', sa.Numeric(), nullable=False),
    sa.Column('profdifficulty', sa.Numeric(), nullable=False),
    sa.Column('classdifficulty', sa.Numeric(), nullable=False),
    sa.Column('quality', sa.Numeric(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_reviews')
    ### end Alembic commands ###