"""make-project_id-not-nullable-milestones-table

Revision ID: cc190b20fdee
Revises: 94449a050b79
Create Date: 2023-03-20 08:55:25.993033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc190b20fdee'
down_revision = '94449a050b79'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('milestones', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('milestones', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
