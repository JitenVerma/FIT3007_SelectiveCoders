from models.Subject import Subject
from models.BidAdditionalInfo import BidAdditionalInfo
from models.Message import Message

class Bid:
    def __init__(self, bidData):
        self.id = bidData['id']
        self.type = bidData['type']
        self.initiator = bidData['initiator']['id']
        self.dateCreated = bidData['dateCreated']
        self.dateClosedDown = bidData['dateClosedDown']
        self.subject = Subject(bidData['subject'])
        self.additionalInfo = BidAdditionalInfo(bidAdditionalInfoData=bidData['additionalInfo'])
        self.messages = []
        
        if 'messages' in bidData:
            for i in range (0, len(bidData['messages'])):
                if not 'bidId' in bidData['messages'][i]:
                    bidData['messages'][i]['bidId'] = self.id
                self.messages.append(Message(bidData['messages'][i]))

    def getId(self):
        return self.id
    
    def getType(self):
        return self.type

    def getInitiator(self):
        return self.initiator

    def getDateCreated(self):
        return self.dateCreated

    def getDateClosedDown(self):
        return self.dateClosedDown

    def getSubject(self):
        return self.subject

    def getAdditionalInfo(self):
        return self.additionalInfo

    def getMessages(self):
        return self.messages