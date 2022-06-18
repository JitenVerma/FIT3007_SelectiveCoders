from models.Competency import Competency
from models.Qualification import Qualification
from models.UserAdditionalInfo import UserAdditionalInfo
from models.Bid import Bid

class User:
    def __init__(self, userData):
        self.id = userData['id']
        self.givenName = userData['givenName']
        self.familyName = userData['familyName']
        self.userName = userData['userName']
        self.isStudent = userData['isStudent']
        self.isTutor = userData['isTutor']
        self.competencies = None
        self.qualifications = None
        self.initiatedBids = None
        self.additionalInfo = UserAdditionalInfo(userData['additionalInfo'])

        if 'competencies' in userData:
            self.competencies = []
            for i in range (0, len(userData['competencies'])):
                self.competencies.append(Competency(userData['competencies'][i]))
        
        if 'qualifications' in userData:
            self.qualifications = []
            for i in range(0, len(userData['qualifications'])):
                self.qualifications.append(Qualification(userData['qualifications'][i]))
        
        if 'initiatedBids' in userData:
            self.initiatedBids = []
            for i in range(0, len(userData['intiatedBids'])):
                self.initiatedBids.append(Bid(userData['initiatedBids'][i]))
    
    def getId(self):
        return self.id
    
    def getGivenName(self):
        return self.givenName

    def getFamilyName(self):
        return self.familyName

    def getUserName(self):
        return self.userName

    def getIsStudent(self):
        return self.isStudent

    def getIsTutor(self):
        return self.isTutor

    def getCompetencies(self):
        return self.competencies

    def getQualifications(self):
        return self.qualifications

    def getInitiatedBids(self):
        return self.initiatedBids
    
    def getAdditionalInfo(self):
        return self.additionalInfo