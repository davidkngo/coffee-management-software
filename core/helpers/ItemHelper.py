from db.model import Item, engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

class ItemHelper:
    @staticmethod
    def createItem(name, price, currency, imageUrl, registryDate):
        item = Item()
        item.name = name
        item.price = price
        item.currency = currency
        item.imageUrl = imageUrl
        item.registryDate = registryDate

        session.add(item)
        session.commit()

    @staticmethod
    def deleteItem(itemId):
        item = session.query(Item).filter(Item.id == itemId).first()
        session.delete(item)
        session.commit()

    @staticmethod
    def editItem(itemId, name=None, price=None, currency=None, imageUrl=None, registryDate=None):
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

    @staticmethod
    def getAllItem():
        items = session.query(Item).all()
        return items

if __name__ == "__main__":
    itemController = ItemHelper()
    # itemController.createItem("ice blend", 1.6, "dollar", "test", "2012-02-20 16:44:14")
    # itemController.deleteItem(4)
    itemController.editItem(5, name="blended", price=1.9, imageUrl="acv")