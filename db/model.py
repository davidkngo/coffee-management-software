from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Menu(Base):
    pass


class OrderItem(Base):
    pass


class Item(Base):
    pass


class Order(Base):
    pass


class Staff(Base):
    pass


class SaleReport(Base):
    pass
