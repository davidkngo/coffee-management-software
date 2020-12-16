from db.model import Item, engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

class ItemController:
    def createItem(self, items):
        for ite in items:
            item = Item()
            item.name = ite['name']
            item.price = ite['price']
            item.currency = ite['currency']
            item.imageUrl = ite['imageUrl']
            item.registryDate = ite['registryDate']

            session.add(item)
        session.commit()

    def deleteItem(self, itemId):
        item = session.query(Item).filter(Item.id == itemId).first()
        session.delete(item)
        session.commit()

    def editItem(self, itemId, name=None, price=None, currency=None, imageUrl=None, registryDate=None):
        item = session.query(Item).filter(Item.id == itemId).first()
        if name:
            item.name = name
        if price:
            item.price = price
        if currency:
            item.currency = currency
        if imageUrl:
            item.imageUrl = imageUrl
        if registryDate:
            item.registryDate = registryDate

        session.commit()


if __name__ == "__main__":
    itemController = ItemController()
    items = [{"name": "chocolate milk", "price": 1.8, "currency": "dollar", "imageUrl": "test1", "registryDate": "2012-02-20 16:44:14"},
             {"name": "cold brew", "price": 1.2, "currency": "dollar", "imageUrl": "test2", "registryDate": "2012-02-20 16:44:14"},
             {"name": "smoothies", "price": 2.0, "currency": "dollar", "imageUrl": "test3", "registryDate": "2012-02-20 16:44:14"},
             {"name": "ice blend", "price": 1.3, "currency": "dollar", "imageUrl": "test4", "registryDate": "2012-02-20 16:44:14"}]
    # itemController.createItem(items)
    itemController.deleteItem(4)
    # itemController.editItem(5, name="blended", price=1.9, imageUrl="acv")