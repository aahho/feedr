"""empty message

Revision ID: 03da332617c3
Revises: c10024ca5685
Create Date: 2017-10-25 23:23:08.947908

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '03da332617c3'
down_revision = 'c10024ca5685'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feed_article_Details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('keyword', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('top_image', sa.Text(), nullable=True),
    sa.Column('sentiment', sa.String(length=255), nullable=True),
    sa.Column('rich_rank', sa.Integer(), nullable=True),
    sa.Column('country_code', sa.String(length=255), nullable=True),
    sa.Column('country_name', sa.String(length=255), nullable=True),
    sa.Column('country_rank', sa.Integer(), nullable=True),
    sa.Column('author', postgresql.ARRAY(sa.Text()), nullable=False),
    sa.Column('feed_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text(u'now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['feed_id'], [u'feeds.id'], ondelete=u'CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feed_article_Details')
    # ### end Alembic commands ###
