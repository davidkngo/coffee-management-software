from db.model import OrderedItems, Item, Order, engine
from sqlalchemy.orm import sessionmaker
import datetime
Session = sessionmaker(bind=engine)

session = Session()

class OrderController:
    def createOrder(self, payment, staffId, items):
        order = Order()
        order.orderDate = str(datetime.datetime.now().strftime("%x")) + " " + str(datetime.datetime.now().strftime("%X"))
        order.paymentMethod = payment
        order.staffId = staffId
        order.status = False   # False means unpaid, True means paid
        for ite in items.values():
            item = session.query(Item).filter(Item.id == ite["id"])
            order.totalPrice += item.price * ite["quantity"]
            for i in range(0, iter["quantity"]):
                order.items.append(item)

        session.add(order)
        session.commit()

    def confirmOrder(self, orderId):
        order = session.query(Order).filter(Order.id == orderId)
        order.status = True

    def editOrder(self):
        print("o")
        # def totalPrice(self, orderId):
