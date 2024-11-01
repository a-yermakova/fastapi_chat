"""add telegram_id field to user model

Revision ID: 5ab5ac088a3d
Revises: 8114b4f4f983
Create Date: 2024-10-27 19:18:35.076354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ab5ac088a3d'
down_revision: Union[str, None] = '8114b4f4f983'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('telegram_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'telegram_id')
    # ### end Alembic commands ###
