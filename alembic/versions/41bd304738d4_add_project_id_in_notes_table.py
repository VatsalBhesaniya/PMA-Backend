"""add-project_id-in-notes-table

Revision ID: 41bd304738d4
Revises: e044fb60b648
Create Date: 2023-03-08 12:13:19.330489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41bd304738d4'
down_revision = 'e044fb60b648'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('project_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'notes', 'projects', ['project_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.drop_column('notes', 'project_id')
    # ### end Alembic commands ###