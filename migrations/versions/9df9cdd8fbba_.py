"""empty message

Revision ID: 9df9cdd8fbba
Revises: a5cffa318ac2
Create Date: 2024-07-01 18:46:46.282359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9df9cdd8fbba'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('species', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('character_id')
    )
    op.create_table('planets',
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('distance', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('planet_id')
    )
    op.create_table('vehicles',
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('number_passengers', sa.Integer(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('vehicle_id')
    )
    op.create_table('user_favourites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('saved_planets', sa.Integer(), nullable=False),
    sa.Column('saved_characters', sa.Integer(), nullable=False),
    sa.Column('saved_vehicles', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['saved_characters'], ['characters.character_id'], ),
    sa.ForeignKeyConstraint(['saved_planets'], ['planets.planet_id'], ),
    sa.ForeignKeyConstraint(['saved_vehicles'], ['vehicles.vehicle_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=250), nullable=False))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('email',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
        batch_op.drop_column('username')

    op.drop_table('user_favourites')
    op.drop_table('vehicles')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###
