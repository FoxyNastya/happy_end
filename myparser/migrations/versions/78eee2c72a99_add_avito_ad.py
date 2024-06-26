"""Add avito ad

Revision ID: 78eee2c72a99
Revises:
Create Date: 2023-04-10 23:06:38.622489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78eee2c72a99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
   op.create_table('avito_ads',
                sa.Column('Id', sa.Integer(), nullable=False),
                sa.Column('Title', sa.String(), nullable=False),
                sa.Column('Price', sa.Float(), nullable=True),
                sa.Column('Square', sa.Float(), nullable=True),
                sa.Column('Address', sa.String(), nullable=True),
                sa.Column('Latitude', sa.Float(), nullable=True),
                sa.Column('Longitude', sa.Float(), nullable=True),
                sa.Column('Link', sa.String(), nullable=True),
                sa.PrimaryKeyConstraint('id')
                )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('avito_ads')
    # ### end Alembic commands ###