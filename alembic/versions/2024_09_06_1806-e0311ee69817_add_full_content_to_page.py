"""add full_content to page

Revision ID: e0311ee69817
Revises: 4287f20e49c5
Create Date: 2024-09-06 18:06:46.748597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0311ee69817'
down_revision: Union[str, None] = '4287f20e49c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('full_content', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page', 'full_content')
    # ### end Alembic commands ###
