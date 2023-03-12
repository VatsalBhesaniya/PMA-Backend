"""add-project_id-in-documents-table

Revision ID: 94449a050b79
Revises: 41bd304738d4
Create Date: 2023-03-09 11:49:13.000286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94449a050b79'
down_revision = '41bd304738d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('documents', sa.Column('project_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'documents', 'projects', ['project_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.drop_column('documents', 'project_id')
    # ### end Alembic commands ###
