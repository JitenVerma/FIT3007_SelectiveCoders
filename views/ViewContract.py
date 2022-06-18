from controllers.ContractController import ContractController
import tkinter as tk
from views.View import View
from datetime import datetime

class ViewContract(View):
    def __init__(self, webService, user, contract):
        self.user = user
        self.contract = contract
        super().__init__(webService)

    def createFrontend(self):
        window = tk.Toplevel()
        window.title("Selected bid")
        self.checkSigned()

        studentSignedLabel = tk.Label(master=window, text = 'Student signed: ' + str(self.contract.getAdditionalInfo().isFirstPartySigned()))
        tutorSignedLabel = tk.Label(master=window, text = 'Tutor signed: ' +  str(self.contract.getAdditionalInfo().isSecondPartySigned()))
        freeLesson = tk.Label(window, text="Free lesson: " + str(self.contract.getAdditionalInfo().isFreeLesson()))
        competencyLabel = tk.Label(window, text="Competency: " + str(self.contract.getAdditionalInfo().getCompetencyRequired()))
        lengthLabel = tk.Label(window, text="Contract Length: " + str(self.contract.getAdditionalInfo().getContractLength()))
        dateCreateLabel = tk.Label(master=window, text = 'Date created: ' + self.contract.getDateCreated())
        if self.contract.getDateSigned() is None:
            dateSignedLabel = tk.Label(master=window, text= 'Date signed: Not signed yet')
        else:
            dateSignedLabel = tk.Label(master=window, text = 'Date signed: ' + self.contract.getDateSigned())
        expiryDateLabel = tk.Label(master=window, text = 'Expiry date: ' + self.contract.getExpiryDate())
        subjectNameLabel = tk.Label(master=window, text = 'Subject name: ' + self.contract.getSubject().getName())
        subjectDescriptionLabel = tk.Label(master=window, text = 'Subject description: ' + self.contract.getSubject().getDescription())
        paymentInfoLabel = tk.Label(master=window, text = 'Payment details: $' + str(self.contract.getPaymentInfo().getPaymentAmount()) + ' ' + self.contract.getPaymentInfo().getPaymentFrequency())
        lessonInfoLabel = tk.Label(master=window, text = 'Sessions per week: ' + str(self.contract.getLessonInfo().getSession_pwk()) + ' , Hours per lesson: ' + str(self.contract.getLessonInfo().getHours_pl()))

        studentSignedLabel.pack()
        tutorSignedLabel.pack()
        freeLesson.pack()
        competencyLabel.pack()
        lengthLabel.pack()
        dateCreateLabel.pack()
        dateSignedLabel.pack()
        expiryDateLabel.pack()
        subjectNameLabel.pack()
        subjectDescriptionLabel.pack()
        paymentInfoLabel.pack()
        lessonInfoLabel.pack()

        # Display sign contract button only if current user has not signed the contract
        if ((self.user.getIsStudent() and not self.contract.getAdditionalInfo().isFirstPartySigned()) or 
            (self.user.getIsTutor() and not self.contract.getAdditionalInfo().isSecondPartySigned())):
                signContractButton = tk.Button(master=window, text="Sign contract", command= lambda: self.signContract(studentSignedLabel, tutorSignedLabel, dateSignedLabel, signContractButton))
                signContractButton.pack()

        window.mainloop()

    def signContract(self, studentSignedLabel, tutorSignedLabel, dateSignedLabel, signContractButton):
        if self.user.getIsStudent() == True:
            self.contract = ContractController.setFirstPartySigned(self.webService, self.contract)
        elif self.user.getIsTutor() == True:
            self.contract = ContractController.setSecondPartySigned(self.webService, self.contract)
        
        # Update text output
        studentSignedLabel['text'] = 'Student signed: ' + str(self.contract.getAdditionalInfo().isFirstPartySigned())
        tutorSignedLabel['text'] = 'Tutor signed: ' +  str(self.contract.getAdditionalInfo().isSecondPartySigned())
        signContractButton.pack_forget()    # Hide sign button

        if self.contract.getDateSigned() is None:
            dateSignedLabel['text'] = 'Date signed: Not signed yet'
        else:
            dateSignedLabel['text'] = 'Date signed: ' + self.contract.getDateSigned()
        
    def checkSigned(self):
        if self.contract.getAdditionalInfo().isFirstPartySigned():
            if self.contract.getAdditionalInfo().isSecondPartySigned():
                if self.contract.getDateSigned() == None:
                    ContractController.signContract(self.webService, self.contract.getId(), (datetime.now()).isoformat())
                    self.contract = ContractController.getContract(self.webService, self.contract.getId())