"""first migration

Revision ID: abd403305284
Revises: 
Create Date: 2024-10-02 17:53:19.892995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abd403305284'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kittens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('breed', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_kittens'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('kittens')
    # ### end Alembic commands ###
