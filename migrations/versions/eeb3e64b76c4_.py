"""empty message

Revision ID: eeb3e64b76c4
Revises: d1db8dcc190d
Create Date: 2018-05-03 16:24:30.369255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeb3e64b76c4'
down_revision = 'd1db8dcc190d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    roles_table = op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    accounts_table = op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('emails', sa.String(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_emails'), 'accounts', ['emails'], unique=True)
    op.create_index(op.f('ix_accounts_username'), 'accounts', ['username'], unique=True)
    op.bulk_insert(roles_table,
            [
                {'id':1, 'display_name':'ADMIN'},
                {'id':2, 'display_name':'USER'}
            ]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_accounts_username'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_emails'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_table('roles')
    # ### end Alembic commands ###
