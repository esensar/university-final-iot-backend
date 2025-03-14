"""empty message

Revision ID: 764de3c39771
Revises: 43e5ad1c4393
Create Date: 2018-11-03 15:00:36.463124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '764de3c39771'
down_revision = '43e5ad1c4393'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('access_levels', sa.Column('created_at', sa.DateTime(),
        nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('access_levels', sa.Column('modified_at', sa.DateTime(),
        nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('device_associations', sa.Column('created_at', sa.DateTime(),
        nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('device_associations', sa.Column('modified_at',
        sa.DateTime(), nullable=False,
        server_default=sa.func.current_timestamp()))
    op.add_column('device_types', sa.Column('created_at', sa.DateTime(),
        nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('device_types', sa.Column('modified_at', sa.DateTime(),
        nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('roles', sa.Column('created_at', sa.DateTime(),
        nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('roles', sa.Column('modified_at', sa.DateTime(),
        nullable=False, server_default=sa.func.current_timestamp()))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'modified_at')
    op.drop_column('roles', 'created_at')
    op.drop_column('device_types', 'modified_at')
    op.drop_column('device_types', 'created_at')
    op.drop_column('device_associations', 'modified_at')
    op.drop_column('device_associations', 'created_at')
    op.drop_column('access_levels', 'modified_at')
    op.drop_column('access_levels', 'created_at')
    # ### end Alembic commands ###
