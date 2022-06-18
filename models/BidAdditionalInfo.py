from models.LessonInfo import LessonInfo
from models.PaymentInfo import PaymentInfo

class BidAdditionalInfo:
    def __init__(self, minimumCompetency=None, lessonInfo=None, paymentInfo=None, bidAdditionalInfoData=None):
        if bidAdditionalInfoData is None:
            self.minimumCompetency = minimumCompetency
            self.lessonInfo = lessonInfo
            self.paymentInfo = paymentInfo
        elif bidAdditionalInfoData is not None:
            self.minimumCompetency = None
            self.lessonInfo = None
            self.paymentInfo = None

            if 'minimumCompetency' in bidAdditionalInfoData:
                self.minimumCompetency = bidAdditionalInfoData['minimumCompetency']
            
            if 'lessonInfo' in bidAdditionalInfoData:
                self.lessonInfo = LessonInfo(bidAdditionalInfoData['lessonInfo'])
            
            if 'paymentInfo' in bidAdditionalInfoData:
                self.paymentInfo = PaymentInfo(bidAdditionalInfoData['paymentInfo'])
    
    def toJSONObject(self):
        return {
            "minimumCompetency": self.minimumCompetency,
            "lessonInfo": self.lessonInfo.toJSONObject(),
            "paymentInfo": self.paymentInfo.toJSONObject()
        }

    def getMinimumCompetency(self):
        return self.minimumCompetency

    def getLessonInfo(self):
        return self.lessonInfo

    def getPaymentInfo(self):
        return self.paymentInfo