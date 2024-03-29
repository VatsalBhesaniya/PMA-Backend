"""remove-member-status-table

Revision ID: 3132a3b38950
Revises: a04c2fcbe9eb
Create Date: 2023-03-06 07:17:00.881915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3132a3b38950'
down_revision = 'a04c2fcbe9eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member_status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member_status',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='member_status_pkey')
    )
    # ### end Alembic commands ###
