"""empty message

Revision ID: 4945e4c8fbca
Revises: ae43d7caad52
Create Date: 2018-10-10 22:50:41.087670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4945e4c8fbca'
down_revision = 'ae43d7caad52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dashboards', sa.Column('active', sa.Boolean(),
        nullable=False, server_default='False'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dashboards', 'active')
    # ### end Alembic commands ###
