from db.model import Item, engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

class ItemHelper:
    def createItem(self, name, price, currency, imageUrl, registryDate):
        item = Item()
        item.name = name
        item.price = price
        item.currency = currency
        item.imageUrl = imageUrl
        item.registryDate = registryDate

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
    itemController = ItemHelper()
    # itemController.createItem("ice blend", 1.6, "dollar", "test", "2012-02-20 16:44:14")
    # itemController.deleteItem(4)
    itemController.editItem(5, name="blended", price=1.9, imageUrl="acv")