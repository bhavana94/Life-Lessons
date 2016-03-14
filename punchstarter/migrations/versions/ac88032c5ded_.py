"""empty message

Revision ID: ac88032c5ded
Revises: afc7cd88656c
Create Date: 2016-03-14 13:17:29.330394

"""

# revision identifiers, used by Alembic.
revision = 'ac88032c5ded'
down_revision = 'afc7cd88656c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Projects', sa.Column('image_filename', sa.String(length=200), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Projects', 'image_filename')
    ### end Alembic commands ###
