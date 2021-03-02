"""Add order completion column

Revision ID: abfe4ce4e17f
Revises: 18eb68a33052
Create Date: 2021-03-01 18:14:39.311010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "abfe4ce4e17f"
down_revision = "18eb68a33052"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("orders", sa.Column("complete", sa.Boolean(), nullable=False))
    op.create_unique_constraint(None, "orders", ["order_id"])


def downgrade():
    op.drop_constraint(None, "orders", type_="unique")
    op.drop_column("orders", "complete")
