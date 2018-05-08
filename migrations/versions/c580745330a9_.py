"""empty message

Revision ID: c580745330a9
Revises: 7e9220844b2f
Create Date: 2018-05-08 10:34:20.757478

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c580745330a9'
down_revision = '7e9220844b2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('device_type', sa.Integer(), nullable=True),
    sa.Column('configuration', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['device_type'], ['device_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('accounts', sa.Column('created_at', sa.DateTime(),
        nullable=True))
    op.add_column('accounts', sa.Column('modified_at', sa.DateTime(),
        nullable=True))
    accounts = sa.sql.table('accounts', sa.sql.column('created_at'), sa.sql.column('modified_at'))
    op.execute(accounts.update().values(created_at=sa.func.now(), modified_at=sa.func.now()))
    op.alter_column('accounts', 'created_at', nullable=False)
    op.alter_column('accounts', 'modified_at', nullable=False)
    op.execute('DELETE FROM recordings')
    op.create_foreign_key(None, 'recordings', 'devices', ['device_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recordings', type_='foreignkey')
    op.drop_column('accounts', 'modified_at')
    op.drop_column('accounts', 'created_at')
    op.drop_table('devices')
    op.drop_table('device_types')
    # ### end Alembic commands ###
