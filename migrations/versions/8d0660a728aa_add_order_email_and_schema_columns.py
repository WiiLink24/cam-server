"""Add order email and schema columns

Revision ID: 8d0660a728aa
Revises: db62843cc80b
Create Date: 2021-03-03 15:40:01.170183

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "8d0660a728aa"
down_revision = "db62843cc80b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("orders", sa.Column("email", sa.String(length=127), nullable=True))
    op.add_column("orders", sa.Column("order_schema", sa.UnicodeText(), nullable=True))


def downgrade():
    op.drop_column("orders", "order_schema")
    op.drop_column("orders", "email")
