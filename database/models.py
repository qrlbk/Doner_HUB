"""Database models for the application."""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

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

    ingredients = relationship("Ingredient", back_populates="dish")
    order_items = relationship("Order", back_populates="dish")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    name = Column(String, nullable=False)

    dish = relationship("Dish", back_populates="ingredients")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    dish = relationship("Dish", back_populates="order_items")


class StockMove(Base):
    __tablename__ = "stock_moves"

    id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, nullable=False)
    change = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
