

class UserAdditionalInfo:
    def __init__(self, userAdditionalInfoData):
        self.subscribedBids = []

        if 'subscribedBids' in userAdditionalInfoData:
            self.subscribedBids = userAdditionalInfoData['subscribedBids']

    def toJSON(self):
        return {'subscribedBids' : self.subscribedBids}
    
    def getSubscribedBids(self):
        return self.subscribedBids