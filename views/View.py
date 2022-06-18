from abc import abstractmethod

class View:
    def __init__(self, webService):
        self.webService = webService
        self.createFrontend()

    @abstractmethod
    def createFrontend(self):
        pass