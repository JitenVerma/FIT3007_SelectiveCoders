from datetime import datetime
from models.MessageAdditionalInfo import MessageAdditionalInfo

class PostMessage:
    def __init__(self, bidId, posterId, content, rate, rateType, sessionsPerWeek, hoursPerSession, freeLesson, receiver, contractLength):
        self.bidId = bidId,
        self.posterId = posterId,
        self.datePosted = datetime.now().isoformat()
        self.content = content

        additionalInfo = {
            'lessonInfo': {
                'session_pwk': sessionsPerWeek,
                'hours_pl': hoursPerSession
            },
            'paymentInfo': {
                'paymentAmount': rate,
                'paymentFrequency': rateType
            },
            'receiver': receiver,
            'freeLesson': freeLesson,
            'contractLength' : contractLength
        }

        self.additionalInfo = MessageAdditionalInfo(additionalInfo)

    def toJSONObject(self):
        return {
            "bidId": self.bidId[0],
            "posterId": self.posterId[0],
            "datePosted": self.datePosted,
            "content": self.content,
            "additionalInfo": self.additionalInfo.toJSONObject()
        }