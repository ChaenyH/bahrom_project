"""Redefine Expense model

Revision ID: 56dc65b66ecb
Revises: 1b6a3cb1f746
Create Date: 2024-12-20 02:50:03.466279

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '56dc65b66ecb'
down_revision = '1b6a3cb1f746'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_method', sa.String(length=20), nullable=False))
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('category',
               existing_type=sa.VARCHAR(length=9),
               type_=postgresql.ENUM('식비', '교통', '숙박', '관광', '쇼핑', '기타', name='expense_category'),
               existing_nullable=False)

    with op.batch_alter_table('travel', schema=None) as batch_op:
        batch_op.alter_column('country',
               existing_type=sa.VARCHAR(length=2),
               type_=postgresql.ENUM('한국', '미국', '유럽', '일본', '베트남', '대만', name='country_types'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('travel', schema=None) as batch_op:
        batch_op.alter_column('country',
               existing_type=postgresql.ENUM('한국', '미국', '유럽', '일본', '베트남', '대만', name='country_types'),
               type_=sa.VARCHAR(length=2),
               existing_nullable=False)

    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.alter_column('category',
               existing_type=postgresql.ENUM('식비', '교통', '숙박', '관광', '쇼핑', '기타', name='expense_category'),
               type_=sa.VARCHAR(length=9),
               existing_nullable=False)
        batch_op.alter_column('date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=False)
        batch_op.drop_column('payment_method')

    # ### end Alembic commands ###
