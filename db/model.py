from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __table__ = 'users'

    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    role = Column(Integer)
    orders = relationship('Order', back_populates='orderMadeBy')


class Order(Base):
    __table__ = 'orders'

    id = Column(Integer, primary_key=True)
    orderDate = Column(DateTime)
    orderMadeById = Column(String, ForeignKey('users.id'))
    orderMadeBy = relationship('User', back_populates='orders')
    items = relationship('Item', back_populates='order')


class Item(Base):
    __table__ = 'items'

    orderId = Column(Integer, ForeignKey('orders.id'))
    order = relationship('Order', back_populates='items')
    name = Column(String)
    price = Column(Float)
    currency = Column(String)
    imageUrl = Column(String)
    registryDate = Column(DateTime)
