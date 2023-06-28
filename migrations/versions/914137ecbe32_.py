"""empty message

Revision ID: 914137ecbe32
Revises: 
Create Date: 2023-06-28 02:51:18.295513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '914137ecbe32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('f_name', sa.String(length=120), nullable=False),
    sa.Column('l_name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('hashed_password', sa.String(length=480), nullable=False),
    sa.Column('salt', sa.String(length=250), nullable=False),
    sa.Column('rol', sa.String(length=20), nullable=False),
    sa.Column('url_image', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
