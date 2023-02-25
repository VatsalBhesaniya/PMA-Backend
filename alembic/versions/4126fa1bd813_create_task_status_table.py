"""create-task_status-table

Revision ID: 4126fa1bd813
Revises: 071e7d0c3df9
Create Date: 2023-02-25 09:40:42.503300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4126fa1bd813'
down_revision = '071e7d0c3df9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_status')
    # ### end Alembic commands ###
