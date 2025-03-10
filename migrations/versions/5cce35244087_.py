"""empty message

Revision ID: 5cce35244087
Revises: 4945e4c8fbca
Create Date: 2018-10-22 21:06:48.532624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cce35244087'
down_revision = '4945e4c8fbca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dashboards', sa.Column('name', sa.String(),
        nullable=False, server_default='Legacy dashboard'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dashboards', 'name')
    # ### end Alembic commands ###
