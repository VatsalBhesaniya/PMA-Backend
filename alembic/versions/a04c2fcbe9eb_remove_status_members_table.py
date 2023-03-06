"""remove-status-members-table

Revision ID: a04c2fcbe9eb
Revises: 6cd9e10745d7
Create Date: 2023-03-06 07:16:11.309604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a04c2fcbe9eb'
down_revision = '6cd9e10745d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('members_status_fkey', 'members', type_='foreignkey')
    op.drop_column('members', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('members_status_fkey', 'members', 'member_status', ['status'], ['id'], ondelete='RESTRICT')
    # ### end Alembic commands ###
