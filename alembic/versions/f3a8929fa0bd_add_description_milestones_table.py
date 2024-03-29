"""add-description-milestones-table

Revision ID: f3a8929fa0bd
Revises: bf46d0c9c0a5
Create Date: 2023-02-27 17:02:48.276062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3a8929fa0bd'
down_revision = 'bf46d0c9c0a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('milestones', sa.Column('description_plain_text', sa.String(), nullable=True))
    op.alter_column('milestones', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('milestones', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('milestones', 'description_plain_text')
    # ### end Alembic commands ###
