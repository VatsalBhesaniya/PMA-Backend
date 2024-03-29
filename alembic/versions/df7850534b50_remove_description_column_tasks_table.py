"""remove-description-column-tasks-table

Revision ID: df7850534b50
Revises: 61c148e4f2a5
Create Date: 2023-02-16 18:04:25.232329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df7850534b50'
down_revision = '61c148e4f2a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
