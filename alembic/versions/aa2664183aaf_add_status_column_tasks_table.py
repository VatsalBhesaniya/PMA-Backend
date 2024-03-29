"""add-status-column-tasks-table

Revision ID: aa2664183aaf
Revises: 4126fa1bd813
Create Date: 2023-02-25 09:51:25.456456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa2664183aaf'
down_revision = '4126fa1bd813'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('status', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tasks', 'task_status', ['status'], ['id'], ondelete='RESTRICT')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'status')
    # ### end Alembic commands ###
