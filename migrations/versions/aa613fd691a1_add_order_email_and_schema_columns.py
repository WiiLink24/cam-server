"""Add order email and schema columns

Revision ID: aa613fd691a1
Revises: db62843cc80b
Create Date: 2021-03-02 20:56:37.154317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aa613fd691a1"
down_revision = "db62843cc80b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("orders", sa.Column("email", sa.String(length=127)))
    op.add_column("orders", sa.Column("order_schema", sa.UnicodeText()))


def downgrade():
    op.drop_column("orders", "email")
    op.drop_column("orders", "order_schema")
