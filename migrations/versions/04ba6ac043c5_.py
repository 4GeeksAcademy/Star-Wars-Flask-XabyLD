"""empty message

Revision ID: 04ba6ac043c5
Revises: 9df9cdd8fbba
Create Date: 2024-07-05 06:41:47.742444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04ba6ac043c5'
down_revision = '9df9cdd8fbba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_favourites', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('saved_planets',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('saved_characters',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('saved_vehicles',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_favourites', schema=None) as batch_op:
        batch_op.alter_column('saved_vehicles',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('saved_characters',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('saved_planets',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
