class PostBid:
    def __init__(self, type, initiatorId, dateCreated, subjectId, additionalInfo):
        self.type = type
        self.initiatorId = initiatorId
        self.dateCreated = dateCreated
        self.subjectId = subjectId         
        self.additionalInfo = additionalInfo

    def toJSONObject(self):
        return {
            "type": self.type,
            "initiatorId": self.initiatorId,
            "dateCreated": self.dateCreated,
            "subjectId": self.subjectId,
            "additionalInfo": self.additionalInfo.toJSONObject()
        }