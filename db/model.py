from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
engine = create_engine("mysql://root:12345@localhost/coffeeshopmanagement", echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(50))
    role = Column(Integer)
    # orders = relationship('Order', back_populates='orderMadeBy')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    staffId = Column(Integer, ForeignKey('users.id'))
    items = relationship('Item', secondary='orderedItems')  # Many to many relation ship with Items, stored in orderedItems

    orderDate = Column(DateTime)
    paymentMethod = Column(String(50))
    totalPrice = Column(Integer)
    status = Column(Boolean)

    staff = relationship('User', back_populates='orders')
    # items = relationship('Item', back_populates='order')

class Item(Base):   # IMPORTANT NOTE: Item and order should be of ONE TO MANY relationship, since at
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    # orderId = Column(Integer, ForeignKey('orders.id'))
    orders = relationship('Order', secondary='orderedItems')    # Many to many relation ship with Items, stored in orderedItems

    name = Column(String(50))
    price = Column(Float)
    currency = Column(String(50))
    imageUrl = Column(String(50))
    registryDate = Column(DateTime)

class OrderedItems(Base):
    __tablename__ = 'orderedItems'

    orderId = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    itemId = Column(Integer, ForeignKey('items.id'), primary_key=True)


# User.orders = relationship('Order', order_by=Order.id, back_populates='users')  # One user (staff) - many orders relationship
# Base.metadata.create_all(engine)

if __name__ == '__main__':
    User.orders = relationship('Order', order_by=Order.id, back_populates='users')  # One user (staff) - many orders relationship
    Base.metadata.create_all(engine)
