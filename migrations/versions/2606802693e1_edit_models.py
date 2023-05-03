"""edit  models

Revision ID: 2606802693e1
Revises: edd54331d858
Create Date: 2023-05-03 11:32:48.183739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2606802693e1'
down_revision = 'edd54331d858'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_main', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_column('id_main')

    # ### end Alembic commands ###