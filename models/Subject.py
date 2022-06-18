from models.Competency import Competency

class Subject:
    def __init__(self, subjectData):
        self.id = subjectData['id']
        self.name = subjectData['name']
        self.description = subjectData['description']
        
        self.competencies = None
        if 'competencies' in subjectData:
            self.competencies = []
            for i in range(0, len(subjectData['competencies'])):
                self.competencies.append(Competency(subjectData['competencies'][i]))

    def getId(self):
        return self.id
    
    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getCompetencies(self):
        return self.competencies