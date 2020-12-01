from db.model import OrderedItems, Item, Order, engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

class OrderController:
    def __init__(self):
        self.order = Order()
        self.total = 0

    def createOrder(self, items):
        for item in items:
            self.order.items.append(item)
            self.total += item.price

    # def totalPrice(self, orderId):

