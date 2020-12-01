from db.model import Order
import datetime

class OrderDao:
    def __init__(self, orderDate=datetime.datetime.now(), status=False, staffId=None):
        self.a = 0

