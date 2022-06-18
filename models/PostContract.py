class PostContract:
    def __init__(self, firstPartyId, secondPartyId, subjectId, dateCreated, expiryDate, paymentInfo, lessonInfo, contractAdditionalInfo):
        self.firstPartyId = firstPartyId
        self.secondPartyId = secondPartyId
        self.subjectId = subjectId
        self.dateCreated = dateCreated
        self.expiryDate = expiryDate
        self.paymentInfo = paymentInfo
        self.lessonInfo = lessonInfo
        self.additionalInfo = contractAdditionalInfo

    def toJSONObject(self):
        return {
            'firstPartyId' : self.firstPartyId,
            'secondPartyId' : self.secondPartyId,
            'subjectId' : self.subjectId,
            'dateCreated' : self.dateCreated,
            'expiryDate' : self.expiryDate,
            'paymentInfo' : self.paymentInfo.toJSONObject(),
            'lessonInfo' : self.lessonInfo.toJSONObject(),
            'additionalInfo' : self.additionalInfo.toJSONObject()
        }