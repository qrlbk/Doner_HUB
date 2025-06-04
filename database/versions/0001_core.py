"""# database/versions/0001_core.py
create_core_tables"""
from alembic import op
import sqlalchemy as sa

revision = "0001_core"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("tg_id", sa.BigInteger, unique=True, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("role", sa.String, nullable=False),
    )
    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("visible", sa.Boolean, server_default=sa.true()),
    )
    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("quantity", sa.Float, server_default="0"),
    )
    op.create_table(
        "dish_ingredients",
        sa.Column("dish_id", sa.Integer, sa.ForeignKey("dishes.id"), primary_key=True),
        sa.Column("ingredient_id", sa.Integer, sa.ForeignKey("ingredients.id"), primary_key=True),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("status", sa.String, nullable=False, server_default="created"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id")),
        sa.Column("dish_id", sa.Integer, sa.ForeignKey("dishes.id")),
        sa.Column("quantity", sa.Integer, nullable=False),
    )
    op.create_table(
        "stock_moves",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ingredient_id", sa.Integer, sa.ForeignKey("ingredients.id")),
        sa.Column("change", sa.Float, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        "gpt_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("message", sa.String, nullable=False),
        sa.Column("role", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        "slots",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("start_time", sa.DateTime, nullable=False),
        sa.Column("end_time", sa.DateTime, nullable=False),
        sa.Column("is_booked", sa.Boolean, server_default=sa.false()),
    )
    op.create_table(
        "masters",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
    )
    op.create_table(
        "services",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("price", sa.Float, nullable=False),
    )
    op.create_table(
        "master_services",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("master_id", sa.Integer, sa.ForeignKey("masters.id")),
        sa.Column("service_id", sa.Integer, sa.ForeignKey("services.id")),
    )


def downgrade() -> None:
    op.drop_table("master_services")
    op.drop_table("services")
    op.drop_table("masters")
    op.drop_table("slots")
    op.drop_table("gpt_logs")
    op.drop_table("stock_moves")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("dish_ingredients")
    op.drop_table("ingredients")
    op.drop_table("dishes")
    op.drop_table("users")
