from models.MessageAdditionalInfo import MessageAdditionalInfo

class Message:
    def __init__(self, messageData):
        self.id = messageData['id']
        self.bidId = messageData['bidId']
        self.poster = messageData['poster']['id']
        self.datePosted = messageData['datePosted']
        self.dateLastEdited = messageData['dateLastEdited']
        self.content = messageData['content']
        self.additionalInfo = MessageAdditionalInfo(messageData['additionalInfo'])
    
    def getId(self):
        return self.id

    def getBidId(self):
        return self.bidId

    def getPoster(self):
        return self.poster

    def getDatePosted(self):
        return self.datePosted

    def getDateLastEdited(self):
        return self.dateLastEdited

    def getContent(self):
        return self.content

    def getAdditionalInfo(self):
        return self.additionalInfo