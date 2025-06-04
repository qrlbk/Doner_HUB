"""# database/models.py
SQLAlchemy models for Doner HUB."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    visible = Column(Boolean, default=True)

    ingredients = relationship(
        "Ingredient", secondary="dish_ingredients", back_populates="dishes"
    )
    order_items = relationship("OrderItem", back_populates="dish")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Float, default=0)

    dishes = relationship(
        "Dish", secondary="dish_ingredients", back_populates="ingredients"
    )
    stock_moves = relationship("StockMove", back_populates="ingredient")


class DishIngredient(Base):
    __tablename__ = "dish_ingredients"

    dish_id = Column(Integer, ForeignKey("dishes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, nullable=False, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    dish = relationship("Dish", back_populates="order_items")


class StockMove(Base):
    __tablename__ = "stock_moves"

    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    change = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    ingredient = relationship("Ingredient", back_populates="stock_moves")


class GPTLog(Base):
    __tablename__ = "gpt_logs"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False)


class Master(Base):
    __tablename__ = "masters"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    services = relationship("MasterService", back_populates="master")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    masters = relationship("MasterService", back_populates="service")


class MasterService(Base):
    __tablename__ = "master_services"

    id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey("masters.id"))
    service_id = Column(Integer, ForeignKey("services.id"))

    master = relationship("Master", back_populates="services")
    service = relationship("Service", back_populates="masters")
