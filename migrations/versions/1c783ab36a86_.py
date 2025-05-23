"""empty message

Revision ID: 1c783ab36a86
Revises: 388820048e94
Create Date: 2025-02-12 23:42:58.630968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c783ab36a86'
down_revision = '388820048e94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('commission', sa.String(length=20), nullable=False),
    sa.Column('mazdoori', sa.String(length=20), nullable=False),
    sa.Column('market_fees', sa.String(length=20), nullable=False),
    sa.Column('rent', sa.String(length=20), nullable=False),
    sa.Column('munshiyaana', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
