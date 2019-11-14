"""empty message

Revision ID: c77cf7c2f3c8
Revises: 8e02c1140792
Create Date: 2019-11-13 19:12:51.804829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c77cf7c2f3c8'
down_revision = '8e02c1140792'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plantTemperature', sa.Integer(), nullable=False),
    sa.Column('soilMoisture', sa.Integer(), nullable=False),
    sa.Column('plantLux', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensor')
    # ### end Alembic commands ###
