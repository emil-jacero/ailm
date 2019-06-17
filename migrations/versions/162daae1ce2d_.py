"""empty message

Revision ID: 162daae1ce2d
Revises: 9390d464bf6c
Create Date: 2019-05-20 11:42:18.269574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '162daae1ce2d'
down_revision = '9390d464bf6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'distro', ['name'])
    op.create_unique_constraint(None, 'image', ['sha256'])
    op.create_unique_constraint(None, 'release', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'release', type_='unique')
    op.drop_constraint(None, 'image', type_='unique')
    op.drop_constraint(None, 'distro', type_='unique')
    # ### end Alembic commands ###
