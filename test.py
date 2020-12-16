class Object(object):
    def __init__(self):
        self._id = 0

    def increaseId(self):
        self._id += 1
        return self._id

    @staticmethod
    def print():
        print("Hello World")

print(Object.__name__)

controller = dict()
controller[Object.__name__] = Object


controller[Object.__name__].print()