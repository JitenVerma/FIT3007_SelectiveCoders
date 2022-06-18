class PaymentInfo:
    def __init__(self, paymentInfoData):
        self.paymentAmount = paymentInfoData['paymentAmount']
        self.paymentFrequency = paymentInfoData['paymentFrequency']
    
    def toJSONObject(self):
        return {
            "paymentAmount": self.paymentAmount,
            "paymentFrequency": self.paymentFrequency
        }
    
    def getPaymentAmount(self):
        return self.paymentAmount

    def getPaymentFrequency(self):
        return self.paymentFrequency