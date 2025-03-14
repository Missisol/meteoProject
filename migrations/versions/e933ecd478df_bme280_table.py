"""bme280 table

Revision ID: e933ecd478df
Revises: 
Create Date: 2025-02-28 14:41:25.228378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e933ecd478df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bme280',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('humidity', sa.Float(), nullable=False),
    sa.Column('pressure', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('bme280', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_bme280_created_at'), ['created_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bme280', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_bme280_created_at'))

    op.drop_table('bme280')
    # ### end Alembic commands ###
