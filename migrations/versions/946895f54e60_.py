"""empty message

Revision ID: 946895f54e60
Revises: ccb8bdaae573
Create Date: 2024-07-06 15:29:10.429330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '946895f54e60'
down_revision = 'ccb8bdaae573'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_favourites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_personaje', sa.Integer(), nullable=True))
        batch_op.drop_constraint('user_favourites_character_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'characters', ['id_personaje'], ['character_id'])
        batch_op.drop_column('character_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_favourites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_favourites_character_id_fkey', 'characters', ['character_id'], ['character_id'])
        batch_op.drop_column('id_personaje')

    # ### end Alembic commands ###
