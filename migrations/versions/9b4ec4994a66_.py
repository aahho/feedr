"""empty message

Revision ID: 9b4ec4994a66
Revises: d387ba0b2980
Create Date: 2017-11-05 15:03:18.737216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b4ec4994a66'
down_revision = 'd387ba0b2980'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'feed_article_details_feed_article_id_fkey', 'feed_article_details', type_='foreignkey')
    op.drop_constraint(u'feed_articles_feed_id_fkey', 'feed_articles', type_='foreignkey')
    op.drop_constraint(u'feed_category_feed_id_fkey', 'feed_category', type_='foreignkey')
    op.drop_constraint(u'feeds_app_id_fkey', 'feeds', type_='foreignkey')
    op.alter_column('apps', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100))
    op.alter_column('feed_article_details', 'feed_article_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               nullable=True)
    op.alter_column('feed_article_details', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100))
    op.alter_column('feed_articles', 'feed_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               nullable=True)
    op.alter_column('feed_articles', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100))
    op.alter_column('feed_category', 'feed_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('feeds', 'app_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               nullable=True)
    op.alter_column('feeds', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               existing_server_default=sa.text(u"nextval('feeds_id_seq'::regclass)"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('feeds', 'id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               existing_server_default=sa.text(u"nextval('feeds_id_seq'::regclass)"))
    op.alter_column('feeds', 'app_id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               nullable=False)
    op.alter_column('feed_category', 'feed_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('feed_articles', 'id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER())
    op.alter_column('feed_articles', 'feed_id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               nullable=False)
    op.alter_column('feed_article_details', 'id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER())
    op.alter_column('feed_article_details', 'feed_article_id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               nullable=False)
    op.alter_column('apps', 'id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER())
    op.create_foreign_key(u'feeds_app_id_fkey', 'feeds', 'apps', ['app_id'], ['id'], ondelete=u'CASCADE')
    op.create_foreign_key(u'feed_category_feed_id_fkey', 'feeds', 'feed_category', ['feed_id'], ['id'], ondelete=u'CASCADE')
    op.create_foreign_key(u'feed_articles_feed_id_fkey', 'feed_articles', 'feeds', ['feed_id'], ['id'], ondelete=u'CASCADE')
    op.create_foreign_key(u'feed_article_details_feed_article_id_fkey', 'feed_article_details', 'feed_articles', ['feed_article_id'], ['id'], ondelete=u'CASCADE')
    # ### end Alembic commands ###