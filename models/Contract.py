from models.Subject import Subject
from models.PaymentInfo import PaymentInfo
from models.LessonInfo import LessonInfo
from models.ContractAdditionalInfo import ContractAdditionalInfo
from models.User import User

class Contract:
    def __init__(self, contractData):
        self.id = contractData['id']
        self.firstParty = User(contractData['firstParty'])
        self.secondParty = User(contractData['secondParty'])
        self.subject = Subject(contractData['subject'])
        self.dateCreated = contractData['dateCreated']
        self.expiryDate = contractData['expiryDate']
        self.dateSigned = contractData['dateSigned']

        self.paymentInfo = None
        if contractData['paymentInfo'] != {}:
            self.paymentInfo = PaymentInfo(contractData['paymentInfo'])

        self.lessonInfo = None
        if contractData['lessonInfo'] != {}:
            self.lessonInfo = LessonInfo(contractData['lessonInfo'])

        self.additionalInfo = None
        if contractData['additionalInfo'] != {}:
            self.additionalInfo = ContractAdditionalInfo(jsonObj=contractData['additionalInfo'])

    def getId(self):
        return self.id
    
    def getFirstParty(self):
        return self.firstParty

    def getSecondParty(self):
        return self.secondParty

    def getSubject(self):
        return self.subject

    def getDateCreated(self):
        return self.dateCreated
    
    def getExpiryDate(self):
        return self.expiryDate

    def getDateSigned(self):
        return self.dateSigned

    def getPaymentInfo(self):
        return self.paymentInfo

    def getLessonInfo(self):
        return self.lessonInfo

    def getAdditionalInfo(self):
        return self.additionalInfo
    
    def setDateSigned(self, dateSigned):
        self.dateSigned = dateSigned