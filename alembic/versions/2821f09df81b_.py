"""empty message

Revision ID: 2821f09df81b
Revises: 862431bd1691
Create Date: 2023-01-06 12:32:08.570729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2821f09df81b'
down_revision = '862431bd1691'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=3), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_operations_id'), 'operations', ['id'], unique=False)
    op.create_table('api_managers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('api_operations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bank_name', sa.String(), nullable=True),
    sa.Column('operation_wrapper_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['operation_wrapper_id'], ['operations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_operations_id'), 'api_operations', ['id'], unique=False)
    op.create_table('manual_managers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('manual_operations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('unix_time', sa.Integer(), nullable=True),
    sa.Column('mcc', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('operation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['operation_id'], ['operations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_manual_operations_id'), 'manual_operations', ['id'], unique=False)
    op.create_table('api_opers_assc',
    sa.Column('api_manager_id', sa.Integer(), nullable=True),
    sa.Column('operation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['api_manager_id'], ['api_managers.id'], ),
    sa.ForeignKeyConstraint(['operation_id'], ['operations.id'], )
    )
    op.create_table('man_opers_assc',
    sa.Column('man_manager_id', sa.Integer(), nullable=True),
    sa.Column('operation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['man_manager_id'], ['manual_managers.id'], ),
    sa.ForeignKeyConstraint(['operation_id'], ['operations.id'], )
    )
    op.create_table('monobank_managers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['api_managers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('monobank_operations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bank_id', sa.String(), nullable=True),
    sa.Column('unix_time', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('mcc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['api_operations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('monobank_operations')
    op.drop_table('monobank_managers')
    op.drop_table('man_opers_assc')
    op.drop_table('api_opers_assc')
    op.drop_index(op.f('ix_manual_operations_id'), table_name='manual_operations')
    op.drop_table('manual_operations')
    op.drop_table('manual_managers')
    op.drop_index(op.f('ix_api_operations_id'), table_name='api_operations')
    op.drop_table('api_operations')
    op.drop_table('api_managers')
    op.drop_index(op.f('ix_operations_id'), table_name='operations')
    op.drop_table('operations')
    # ### end Alembic commands ###