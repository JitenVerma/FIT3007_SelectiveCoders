from models.LessonInfo import LessonInfo
from models.PaymentInfo import PaymentInfo

class MessageAdditionalInfo:
    def __init__(self, messageAdditionalInfoData):
        self.lessonInfo = None
        self.paymentInfo = None
        self.receiver = None
        self.freeLesson = False
        self.contractLength = 6

        if 'lessonInfo' in messageAdditionalInfoData:
            self.lessonInfo = LessonInfo(messageAdditionalInfoData['lessonInfo'])
        
        if 'paymentInfo' in messageAdditionalInfoData:
            self.paymentInfo = PaymentInfo(messageAdditionalInfoData['paymentInfo'])
        
        if 'receiver' in messageAdditionalInfoData:
            self.receiver = messageAdditionalInfoData['receiver']
        
        if 'freeLesson' in messageAdditionalInfoData:
            self.freeLesson = messageAdditionalInfoData['freeLesson']
        
        if 'contractLength' in messageAdditionalInfoData:
            self.contractLength = messageAdditionalInfoData['contractLength']
    
    def toJSONObject(self):
        return {
            "lessonInfo": self.lessonInfo.toJSONObject(),
            "paymentInfo": self.paymentInfo.toJSONObject(),
            "receiver": self.receiver,
            "freeLesson": self.freeLesson,
            "contractLength": self.contractLength,
        }

    def getLessonInfo(self):
        return self.lessonInfo

    def getPaymentInfo(self):
        return self.paymentInfo
    
    def getReceiver(self):
        return self.receiver

    def getFreeLesson(self):
        return self.freeLesson
    
    def getContractLength(self):
        return self.contractLength