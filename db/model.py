from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import datetime
engine = create_engine("mysql://root:12345@localhost/coffeeshopmanagement", echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(50))
    role = Column(Integer)

    orders = relationship('Order')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    staffId = Column(Integer, ForeignKey('users.id'))
    items = relationship('OrderedItems', back_populates='order', cascade='all, delete-orphan')  # Many to many relation ship with Items, stored in orderedItems

    orderDate = Column(DateTime)
    paymentMethod = Column(String(50))
    totalPrice = Column(Float)
    status = Column(Boolean)

class Item(Base):   # IMPORTANT NOTE: Item and order should be of ONE TO MANY relationship, since at
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    orders = relationship('OrderedItems', back_populates='item', cascade='all, delete-orphan')    # Many to many relation ship with Items, stored in orderedItems

    name = Column(String(50))
    price = Column(Float)
    currency = Column(String(50))
    imageUrl = Column(String(50))
    registryDate = Column(DateTime)

class OrderedItems(Base):
    __tablename__ = 'orderedItems'

    orderId = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    itemId = Column(Integer, ForeignKey('items.id'), primary_key=True)
    item = relationship('Item', back_populates='orders')
    order = relationship('Order', back_populates='items')

    quantity = Column(Integer)


Base.metadata.create_all(engine)
# if __name__ == '__main__':
#     Session = sessionmaker(bind=engine)
#
#     session = Session()
#     order = Order()
#     order.orderDate = str(datetime.datetime.now().strftime("%x")) + " " + str(datetime.datetime.now().strftime("%X"))
#     order.paymentMethod = None
#     order.staffId = 1
#     order.status = False  # False means unpaid, True means paid
#     order.totalPrice = 0
#
#     items = {"item1": {"id": 1, "quantity": 3}, "item2": {"id": 2, "quantity": 2}}
#
#     for ite in items.values():
#         item = session.query(Item).filter(Item.id == ite["id"]).first()
#         print("item is: ", item.price)
#         print("quantity is: ", ite["quantity"])
#         order.totalPrice += item.price * ite["quantity"]
#         print(order.totalPrice)
#
#         orderedItems = OrderedItems(quantity=ite["quantity"])
#         orderedItems.item = item
#         order.items.append(orderedItems)
#
#     session.add(order)
#     session.commit()
