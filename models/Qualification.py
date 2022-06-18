class Qualification:
    def __init__(self, qualificationData):
        self.id = qualificationData['id']
        self.title = qualificationData['title']
        self.description = qualificationData['description']
        self.verified = qualificationData['verified']