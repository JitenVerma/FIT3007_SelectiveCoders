class ContractAdditionalInfo:
    def __init__(self, firstPartySigned=False, secondPartySigned=False, freeLesson=False, competencyRequired=1, contractLength=0, jsonObj=None):
        if jsonObj is None:
            self.firstPartySigned = firstPartySigned
            self.secondPartySigned = secondPartySigned
            self.freeLesson = freeLesson
            self.competencyRequired = competencyRequired
            self.contractLength = contractLength
        elif jsonObj is not None:
            if 'firstPartySigned' in jsonObj:
                self.firstPartySigned = jsonObj['firstPartySigned']
            if 'secondPartySigned' in jsonObj:
                self.secondPartySigned = jsonObj['secondPartySigned']
            if 'freeLesson' in jsonObj:
                self.freeLesson = jsonObj['freeLesson']
            if 'competencyRequired' in jsonObj:
                self.competencyRequired = jsonObj['competencyRequired']   
            if 'contractLength' in jsonObj:
                self.contractLength = jsonObj['contractLength']
            

    def setFirstPartySigned(self):
        self.firstPartySigned = True

    def setSecondPartySigned(self):
        self.secondPartySigned = True

    def setFreeLessonTrue(self):
        self.freeLesson = True

    def isFirstPartySigned(self):
        return self.firstPartySigned
    
    def isSecondPartySigned(self):
        return self.secondPartySigned

    def isFreeLesson(self):
        return self.freeLesson
    
    def getCompetencyRequired(self):
        return self.competencyRequired
    
    def getContractLength(self):
        return self.contractLength

    def toJSONObject(self):
        return {
            'firstPartySigned' : self.firstPartySigned,
            'secondPartySigned' : self.secondPartySigned,
            'freeLesson': self.freeLesson,
            'competencyRequired': self.competencyRequired,
            'contractLength': self.contractLength
        }