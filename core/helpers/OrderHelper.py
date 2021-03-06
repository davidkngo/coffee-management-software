
from sqlalchemy.orm import sessionmaker
from db.model import OrderedItems, Item, Order, engine
import datetime

Session = sessionmaker(bind=engine)

session = Session()

class OrderHelper:
    @staticmethod
    def createOrder(staffId, items):
        order = Order()
        order.orderDate = str(datetime.datetime.now().strftime('%Y-%m-%d')) + " " + str(datetime.datetime.now().strftime("%X"))
        print("\n\n\n\t\t\t__________\n\t\t\tTHE DATE: ", str(datetime.datetime.now().strftime("%x")) + " " + str(datetime.datetime.now().strftime("%X")))
        order.paymentMethod = None
        order.staffId = staffId
        order.status = False   # False means unpaid, True means paid
        order.totalPrice = 0
        for ite in items.values():
            item = session.query(Item).filter(Item.name == ite["name"]).first()

            order.totalPrice += item.price * ite["quantity"]

            orderedItems = OrderedItems(quantity=ite["quantity"])
            orderedItems.item = item

            order.items.append(orderedItems)

        session.add(order)
        session.commit()

    def confirmOrder(self, payment, orderId):
        order = session.query(Order).filter(Order.id == orderId).first()
        order.paymentMethod = payment
        order.status = True
        session.commit()

    def editOrder(self, orderId, items):
        order = session.query(Order).filter(Order.id == orderId).first()
        order.items = []
        order.totalPrice = 0
        for ite in items.values():
            item = session.query(Item).filter(Item.id == ite["id"]).first()
            order.totalPrice += item.price * ite["quantity"]
            orderedItems = OrderedItems(quantity=ite["quantity"])
            orderedItems.item = item

            order.items.append(orderedItems)
        session.commit()


if __name__ == "__main__":
    orderController = OrderHelper()
    items = {"item1": {"name": "smoothies", "quantity": 1}}
    orderController.createOrder(1, items)
    # orderController.editOrder(1, items)
    # orderController.confirmOrder('debit card', 1)
