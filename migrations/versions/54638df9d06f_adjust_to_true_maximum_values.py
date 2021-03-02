"""Adjust to true maximum values

Revision ID: 54638df9d06f
Revises: abfe4ce4e17f
Create Date: 2021-03-02 01:00:50.417794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "54638df9d06f"
down_revision = "abfe4ce4e17f"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "images",
        "image_id",
        existing_type=sa.VARCHAR(length=8),
        type_=sa.String(length=7),
        existing_nullable=False,
    )
    op.alter_column(
        "images",
        "order_id",
        existing_type=sa.VARCHAR(length=8),
        type_=sa.String(length=14),
        existing_nullable=False,
    )
    op.alter_column(
        "orders",
        "order_id",
        existing_type=sa.VARCHAR(length=8),
        type_=sa.String(length=14),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "orders",
        "order_id",
        existing_type=sa.String(length=14),
        type_=sa.VARCHAR(length=8),
        existing_nullable=False,
    )
    op.alter_column(
        "images",
        "order_id",
        existing_type=sa.String(length=14),
        type_=sa.VARCHAR(length=8),
        existing_nullable=False,
    )
    op.alter_column(
        "images",
        "image_id",
        existing_type=sa.String(length=7),
        type_=sa.VARCHAR(length=8),
        existing_nullable=False,
    )
