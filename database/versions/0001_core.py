from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001_core"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tg_id", sa.BigInteger(), unique=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
    )

    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column(
            "visible", sa.Boolean(), server_default=sa.text("true"), nullable=False
        ),
    )

    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("qty", sa.Float(), nullable=False, server_default="0"),
        sa.Column("min_qty", sa.Float(), nullable=False, server_default="0"),
    )

    op.create_table(
        "dish_ingredients",
        sa.Column(
            "dish_id", sa.Integer(), sa.ForeignKey("dishes.id"), primary_key=True
        ),
        sa.Column(
            "ingredient_id",
            sa.Integer(),
            sa.ForeignKey("ingredients.id"),
            primary_key=True,
        ),
        sa.Column("qty", sa.Float(), nullable=False),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("status", sa.String(), nullable=False, server_default="new"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.String(), sa.ForeignKey("orders.id")),
        sa.Column("dish_id", sa.Integer(), sa.ForeignKey("dishes.id")),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
    )

    op.create_table(
        "stock_moves",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ingredient_id", sa.Integer(), sa.ForeignKey("ingredients.id")),
        sa.Column("change", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "gpt_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "masters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
    )

    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
    )

    op.create_table(
        "slots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("master_id", sa.Integer(), sa.ForeignKey("masters.id")),
    )

    op.create_table(
        "master_services",
        sa.Column(
            "master_id", sa.Integer(), sa.ForeignKey("masters.id"), primary_key=True
        ),
        sa.Column(
            "service_id", sa.Integer(), sa.ForeignKey("services.id"), primary_key=True
        ),
    )


def downgrade() -> None:
    op.drop_table("master_services")
    op.drop_table("slots")
    op.drop_table("services")
    op.drop_table("masters")
    op.drop_table("gpt_logs")
    op.drop_table("stock_moves")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("dish_ingredients")
    op.drop_table("ingredients")
    op.drop_table("dishes")
    op.drop_table("users")
