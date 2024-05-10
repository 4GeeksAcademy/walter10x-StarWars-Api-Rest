"""empty message

Revision ID: 2952fdd5e0e8
Revises: eff15c02ac3f
Create Date: 2024-05-10 00:05:42.513401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2952fdd5e0e8'
down_revision = 'eff15c02ac3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('people')
    # ### end Alembic commands ###
