"""empty message

Revision ID: bdbdaf4378cd
Revises: 91b6b2e4afa1
Create Date: 2019-04-22 13:55:19.769238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdbdaf4378cd'
down_revision = '91b6b2e4afa1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('source_url', sa.String(length=200), nullable=False))
    op.drop_column('image', 'url')
    op.drop_column('release', 'company')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('release', sa.Column('company', sa.VARCHAR(length=60), autoincrement=False, nullable=False))
    op.add_column('image', sa.Column('url', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    op.drop_column('image', 'source_url')
    # ### end Alembic commands ###
