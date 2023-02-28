"""update-column-name-milestones-table

Revision ID: 0a5ba8aa069a
Revises: bdafeca0ba0e
Create Date: 2023-02-27 08:07:59.074329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a5ba8aa069a'
down_revision = 'bdafeca0ba0e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('milestones', sa.Column('is_completed', sa.Boolean(), nullable=False))
    op.drop_column('milestones', 'isCompleted')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('milestones', sa.Column('isCompleted', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('milestones', 'is_completed')
    # ### end Alembic commands ###
