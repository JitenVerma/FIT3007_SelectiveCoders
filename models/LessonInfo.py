class LessonInfo:
    def __init__(self, lessonInfoData):
            self.session_pwk = lessonInfoData['session_pwk']
            self.hours_pl = lessonInfoData['hours_pl']
    
    def toJSONObject(self):
        return {
            "session_pwk": self.session_pwk,
            "hours_pl": self.hours_pl
        }

    def getSession_pwk(self):
        return self.session_pwk

    def getHours_pl(self):
        return self.hours_pl