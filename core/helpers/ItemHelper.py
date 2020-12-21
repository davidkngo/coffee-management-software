from db.model import Item, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class ItemHelper:
    @staticmethod
    def createItem(name, price, currency, imageUrl, registryDate, stockQuantity):
        item = Item()
        item.name = name
        item.price = price
        item.currency = currency
        item.imageUrl = imageUrl
        item.registryDate = registryDate
        item.stockQuantity = stockQuantity

        session.add(item)
        session.commit()

    @staticmethod
    def deleteItem(itemId):
        item = session.query(Item).filter(Item.id == itemId).first()
        session.delete(item)
        session.commit()

    @staticmethod
    def editItem(itemId, name=None, price=None, currency=None, imageUrl=None, registryDate=None, stockQuantity=None):
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
        if stockQuantity:
            item.stockQuantity = stockQuantity

        session.commit()

    @staticmethod
    def getAllItem():
        items = session.query(Item).all()
        return items


if __name__ == "__main__":
    itemController = ItemHelper()
    items = [{"name": "ice blend", "price": 1.6, "currency": "dollar", "imageUrl": "test", "registryDate": "2012-02-20 16:44:14", "stockQuantity": 5},
             {"name": "cold brew", "price": 2.0, "currency": "dollar", "imageUrl": "test", "registryDate": "2012-02-20 16:44:14", "stockQuantity": 2},
             {"name": "smoothies", "price": 1.8, "currency": "dollar", "imageUrl": "test", "registryDate": "2012-02-20 16:44:14", "stockQuantity": 1}]
    for i in items:
        itemController.createItem(i["name"], i["price"], i["currency"], i["imageUrl"], i["registryDate"], i["stockQuantity"])
    # itemController.deleteItem(4)
    # itemController.editItem(5, name="blended", price=1.9, imageUrl="acv")
