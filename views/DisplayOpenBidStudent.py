import tkinter as tk
from tkinter import ttk
from views.View import View
from models.ContractAdditionalInfo import ContractAdditionalInfo
from datetime import datetime
from dateutil.relativedelta import relativedelta
from models.PostContract import PostContract
from controllers.UserController import UserController
from controllers.ContractController import ContractController
from controllers.BidController import BidController
from views.ErrorPopup import ErrorPopup

class DisplayOpenBidStudent(View):
    def __init__(self, webService, user, bid):
        self.user = user
        self.bid = bid
        self.messages = bid.getMessages()
        self.deleted = False
        super().__init__(webService)

    def refresh(self, window, bidOffersTable):
        if not self.deleted:
            # Determine currently selected rows
            currentlySelectedMessage = bidOffersTable.focus()
            currentlySelectedMessageId = bidOffersTable.item(currentlySelectedMessage)['text']

            # Empty table
            for i in bidOffersTable.get_children():
                bidOffersTable.delete(i)
            
            # Get fresh bid info from API
            self.bid = BidController.getBid(self.webService, self.bid.getId())
            self.messages = self.bid.getMessages()

            # Display messages on screen
            for i in range(0, len(self.messages)):
                messageId = self.messages[i].getId()
                posterId = self.messages[i].getPoster()

                user = UserController.getUser(self.webService, posterId)
                poster = user.getGivenName() + " " + user.getFamilyName() + " @" + user.getUserName()

                paymentInfo = str(self.messages[i].getAdditionalInfo().getPaymentInfo().getPaymentAmount()) + " " + self.messages[i].getAdditionalInfo().getPaymentInfo().getPaymentFrequency()
                lessonInfo =  str(self.messages[i].getAdditionalInfo().getLessonInfo().getSession_pwk()) + " session(s) per week, " + str(self.messages[i].getAdditionalInfo().getLessonInfo().getHours_pl()) + " hour(s) per session"
                freeLesson = str(self.messages[i].getAdditionalInfo().getFreeLesson())
                contractLength = str(self.messages[i].getAdditionalInfo().getContractLength())

                bidOffersTable.insert("", "end", text=messageId, values=(poster, paymentInfo, lessonInfo, freeLesson, contractLength))
                if messageId == currentlySelectedMessageId:
                            child_id = bidOffersTable.get_children()[-1]
                            bidOffersTable.focus(child_id)
                            bidOffersTable.selection_set(child_id)

            # Refresh screen
            window.update()
        window.after(10000, self.refresh, window, bidOffersTable)

    def createFrontend(self):
        window = tk.Toplevel()
        window.title("Selected bid")

        #Display all bid information on screen
        dateCreatedLabel = tk.Label(master=window, text = "Date Created: " + self.bid.getDateCreated())

        closeDownDate = self.bid.getDateClosedDown()
        if closeDownDate == None:
            closeDownDate = "Not set"
        dateCloseDownLabel = tk.Label(master=window, text = "Date Closing: " + closeDownDate)

        subjectNameLabel = tk.Label(master=window, text="Subject Name: " + self.bid.getSubject().getName())
        subjectDescriptionLabel = tk.Label(master=window, text="Subject Description: " + self.bid.getSubject().getDescription())

        bidAdditionalInfo = self.bid.getAdditionalInfo()

        subjectCompetency = self.bid.getAdditionalInfo().getMinimumCompetency()
        if subjectCompetency == None:
            subjectCompetency = "Not set"
        subjectCompetencyLabel = tk.Label(master=window, text="Minimum Competency: " + subjectCompetency)

        lessonInfo = bidAdditionalInfo.getLessonInfo()
        lessonText = "Not set"
        if lessonInfo != None:
            lessonText = "Lesson Info: " + lessonInfo.getSession_pwk() + " session(s) per week, " + lessonInfo.getHours_pl() + " hour(s) per session"
        lessonInfoLabel = tk.Label(master=window, text=lessonText)

        paymentInfo = bidAdditionalInfo.getPaymentInfo()
        paymentText = "Not set"
        if paymentInfo != None:
            paymentText = paymentInfo.getPaymentAmount() + " " + paymentInfo.getPaymentFrequency()
        paymentInfoLabel = tk.Label(master=window, text="Payment: $" + paymentText)

        #Show offers from tutors
        bidOffersLabel = tk.Label(window, text="Bid Offers")
        bidOffersTable = ttk.Treeview(window, height=5)

        bidOffersTable["columns"] = ("bidder", "paymentInfo", "lessonInfo", "freeLesson", "contractLength")

        bidOffersTable.heading('#0', text='messageId')
        bidOffersTable.heading('bidder', text='bidder')
        bidOffersTable.heading("paymentInfo", text="paymentInfo", anchor=tk.W)
        bidOffersTable.heading("lessonInfo", text="lessonInfo", anchor=tk.W)
        bidOffersTable.heading("freeLesson", text="freeLesson", anchor=tk.W)
        bidOffersTable.heading("contractLength", text="contractLength", anchor=tk.W)

        bidOffersTable.column("freeLesson", width=75)
        bidOffersTable.column("contractLength", width=100)

        contractLengthLabel = tk.Label(master=window, text="Contract length (months):")
        defaultContractLength = tk.StringVar(window)
        contractLengthSpinbox = tk.Spinbox(master=window, values=(3, 6, 12, 24), textvariable=defaultContractLength)
        defaultContractLength.set("6")

        #Select winner button
        selectWinnerButton = tk.Button(window, text='Select winner', width=25, command= lambda: self.selectWinner(bidOffersTable.item(bidOffersTable.focus())['text'], contractLengthSpinbox.get(),window))

        dateCreatedLabel.pack()
        dateCloseDownLabel.pack()
        subjectNameLabel.pack()
        subjectDescriptionLabel.pack()
        subjectCompetencyLabel.pack()
        lessonInfoLabel.pack()
        paymentInfoLabel.pack()
        bidOffersLabel.pack()
        bidOffersTable.pack()
        contractLengthLabel.pack()
        contractLengthSpinbox.pack()
        selectWinnerButton.pack()
        

        window.after(500, self.refresh, window, bidOffersTable)
        window.mainloop()
        
    def selectWinner(self, selectedMessageId, studentContractLength, window):
        for i in range(0, len(self.messages)):
            if self.messages[i].getId() == selectedMessageId:
                message = self.messages[i]
                break
        
        try:
            contractLengthInt = int(studentContractLength)
        except:
            ErrorPopup("Please type integer for contract length in months", self.webService)
            return
        if contractLengthInt < 3:
            contractLengthInt = 3

        firstPartyId = self.user.getId()
        secondPartyId = message.getPoster()
        subjectId = self.bid.getSubject().getId()
        dateCreated = datetime.now().isoformat()
        expiry = datetime.now() + relativedelta(months=contractLengthInt)
        expiryDate = expiry.isoformat()
        paymentInfo = message.getAdditionalInfo().getPaymentInfo()
        lessonInfo = message.getAdditionalInfo().getLessonInfo()
        freeLesson = message.getAdditionalInfo().getFreeLesson()
        additionalInfo = ContractAdditionalInfo(False, False, freeLesson, self.bid.getAdditionalInfo().getMinimumCompetency(), contractLengthInt)

        newContract = PostContract(firstPartyId, secondPartyId, subjectId, dateCreated, expiryDate, paymentInfo, lessonInfo, additionalInfo)
        newContractJSONObject = newContract.toJSONObject()
        postContract = ContractController.addContract(self.webService, newContractJSONObject)
        
        BidController.deleteBid(self.webService, self.bid)
        self.deleted = True
        window.destroy()