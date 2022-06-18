class Competency:
    def __init__(self, competencyData):
        self.id = competencyData['id']
        self.subject = competencyData['subject']['id']
        self.level = competencyData['level']
    
    def getId(self):
        return self.id

    def getSubject(self):
        return self.subject

    def getLevel(self):
        return self.level