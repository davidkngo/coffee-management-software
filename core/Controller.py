class ControllerFactory(object):
    def __init__(self):
        self.__controllers__ = dict()

    def register_controller(self, controller):
        
        key = controller.__name__
        if key not in self.__controllers__.keys():
            self.__controllers__[key] = controller

    def get_controller(self, key):
        if key not in self.__controllers__.keys():
            raise Exception("Controller has not been registered yet")

        return self.__controllers__[key]