from controllers.UserController import UserController
from models.PostContract import PostContract
from models.ContractAdditionalInfo import ContractAdditionalInfo
from dateutil.relativedelta import relativedelta
from views.ErrorPopup import ErrorPopup
import tkinter as tk
from views.View import View
from models.LessonInfo import LessonInfo
from models.PaymentInfo import PaymentInfo
from datetime import datetime
from controllers.ContractController import ContractController

class RenewContract(View):
    """
    Creates the RenewContract view where students can renew a contract.
    Extends the View class
    """

    def __init__(self, webService, contract, activeContracts):
        """
        Constructor initialises some variables and runs the super constructor (which runs createFrontend)
        :param webService: Instance of the WebService object used throughout the application
        :param contract: Contract object of the contract to renew
        :param activeContracts: Count of users active contracts
        :return: None
        """

        self.contract = contract
        self.activeContracts = activeContracts
        super().__init__(webService)
    
    def renew(self, competency, hoursPerLesson, lessonsPerWeek, preferredRate, paymentFrequency, studentContractLength, tutorID, window):
        """
        Submits the new contract to the server and then closes the window.
        :param competency: Int of the required competency level
        :param hoursPerLesson: Int of hours per lesson
        :param lessonsPerWeek: Int of lessons per week
        :param preferredRate: Float of rate
        :param paymentFrequency: String (either Per hour or Per session) to denote payment frequency
        :param window: Tk window object currently used
        :return: None
        """

        if self.activeContracts >= 5:
            ErrorPopup("You have too many active contracts, please delete some.", self.webService)
            return

        try:
            contractLengthInt = int(studentContractLength)
        except:
            ErrorPopup("Please type integer for contract length in months", self.webService)
            return
        
        if contractLengthInt < 3:
            contractLengthInt = 3
        
        secondParty = UserController.getUser(self.webService, tutorID)
        if (not secondParty.getIsTutor()):
            ErrorPopup("The provided tutor ID is not a tutor", self.webService)
            return
        
        subjectId = self.contract.getSubject().getId()
        minimumCompetency = self.contract.getAdditionalInfo().getCompetencyRequired()
        competent = False
        for competency in secondParty.getCompetencies():
            if subjectId == competency.getSubject():
                if int(minimumCompetency) + 2 <= competency.getLevel():
                    competent = True
                    break

        if not competent:
            ErrorPopup("The provided tutor is not competent", self.webService)
            return

        firstPartyId = self.contract.getFirstParty().getId()
        secondPartyId = secondParty.getId()
        subjectId = self.contract.getSubject().getId()
        dateCreated = datetime.now().isoformat()
        expiry = datetime.now() + relativedelta(months=contractLengthInt)
        expiryDate = expiry.isoformat()

        # Adding additional info
        paymentInfo = PaymentInfo({'paymentAmount': preferredRate, 'paymentFrequency': paymentFrequency})
        lessonInfo = LessonInfo({'session_pwk': lessonsPerWeek, 'hours_pl': hoursPerLesson})
        freeLesson = self.contract.getAdditionalInfo().isFreeLesson()
        additionalInfo = ContractAdditionalInfo(False, False, freeLesson, minimumCompetency, contractLengthInt)

        # Create new post contract object and submit it to the server
        newContract = PostContract(firstPartyId, secondPartyId, subjectId, dateCreated, expiryDate, paymentInfo, lessonInfo, additionalInfo)
        newContractJSONObject = newContract.toJSONObject()
        postContract = ContractController.addContract(self.webService, newContractJSONObject)
        
        # Close the current window and to go back to homepage
        window.destroy()

    def createFrontend(self):
        """
        Create the frontend of the RenewContract view
        :return: None
        """
        
        # Instantiate window to be used
        window = tk.Tk()
        window.title('Tutoring system')
        
        deleteButton = tk.Button(window, text='Delete Contract', width=25, command= lambda: self.delete(window))

        # Select tutor
        tutorIdLabel = tk.Label(window, text="Tutor ID:")
        tutorIdEntry = tk.Entry(window, fg="black", bg="white", width=50)
        tutorIdEntry.insert(tk.END, self.contract.getSecondParty().getId())
        
        # Decide required competency level
        requiredCompetencyLevelLabel = tk.Label(window, text="Competency level required:")
        competencyLevelSpinbox = tk.Spinbox(window, from_=1, to_=10)

        # Decide the subject
        subjectLabel = tk.Label(window, text="Subject: " + self.contract.getSubject().getName() + " - " + self.contract.getSubject().getDescription())

        # Decide hours per lesson required
        hoursPerLessonLabel = tk.Label(window, text="Length of lessons required (Hours):")
        hoursPerLessonVar = tk.IntVar(value=self.contract.getLessonInfo().getHours_pl())
        hoursPerLessonSpinbox = tk.Spinbox(window, from_=1, to_=24, textvariable=hoursPerLessonVar)

        # Decide lessons per week
        lessonsPerWeekLabel = tk.Label(window, text="Lessons per week required:")
        lessonsPerWeekVar = tk.IntVar(value=self.contract.getLessonInfo().getSession_pwk())
        lessonsPerWeekSpinbox = tk.Spinbox(window, from_=1, to_=7, textvariable=lessonsPerWeekVar)

        # Decide preferred rate
        preferredRateLabel = tk.Label(window, text="Preferred rate:")
        preferredRateEntry = tk.Entry(window, fg="black", bg="white", width=50)
        preferredRateEntry.insert(tk.END, str(self.contract.getPaymentInfo().getPaymentAmount()))

        # Decide whether preferred rate is per hour or per session
        paymentFrequency = tk.StringVar(window)
        hourRadio = tk.Radiobutton(window, text='Per hour', variable=paymentFrequency, value="Per hour")
        sessionRadio = tk.Radiobutton(window, text='Per session', variable=paymentFrequency, value="Per session")

        if (self.contract.getPaymentInfo().getPaymentFrequency() == "Per session"):
            sessionRadio.select()
        else:
            hourRadio.select()
        
        contractLengthLabel = tk.Label(master=window, text="Contract length (months):")
        contractLengthVar = tk.StringVar(window)
        contractLengthSpinbox = tk.Spinbox(master=window, values=(3, 6, 12, 24), textvariable=contractLengthVar)
        contractLengthVar.set(str(self.contract.getAdditionalInfo().getContractLength()))

        # Post Bid button
        renewButton = tk.Button(window, text='Renew Contract', width=25, command= lambda: self.renew(competencyLevelSpinbox.get(), hoursPerLessonSpinbox.get(), lessonsPerWeekSpinbox.get(), preferredRateEntry.get(), paymentFrequency.get(), contractLengthSpinbox.get(), tutorIdEntry.get(), window))

        # Pack elements onto window       
        deleteButton.pack()
        tutorIdLabel.pack()
        tutorIdEntry.pack()
        requiredCompetencyLevelLabel.pack()
        competencyLevelSpinbox.pack()
        subjectLabel.pack()
        hoursPerLessonLabel.pack()
        hoursPerLessonSpinbox.pack()
        lessonsPerWeekLabel.pack()
        lessonsPerWeekSpinbox.pack()
        preferredRateLabel.pack()
        preferredRateEntry.pack()
        hourRadio.pack()
        sessionRadio.pack()
        contractLengthLabel.pack()
        contractLengthSpinbox.pack()
        renewButton.pack()

        # Start the window mainloop
        window.mainloop()
    
    def delete(self, window):
        ContractController.deleteContract(self.webService, self.contract.getId())
        window.destroy()