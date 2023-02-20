"""update-users-table

Revision ID: be6fd8991927
Revises: 9efb171164f5
Create Date: 2023-02-20 07:58:19.086968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be6fd8991927'
down_revision = '9efb171164f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('description', sa.ARRAY(sa.JSON()), nullable=True))
    op.add_column('tasks', sa.Column('description_plain_text', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('tasks', 'description_plain_text')
    op.drop_column('tasks', 'description')
    # ### end Alembic commands ###
