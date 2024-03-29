"""add-project-relationship-in-milestones-table

Revision ID: bf46d0c9c0a5
Revises: 0a5ba8aa069a
Create Date: 2023-02-27 08:27:03.058630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf46d0c9c0a5'
down_revision = '0a5ba8aa069a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('milestones', sa.Column('project_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'milestones', 'projects', ['project_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'milestones', type_='foreignkey')
    op.drop_column('milestones', 'project_id')
    # ### end Alembic commands ###
