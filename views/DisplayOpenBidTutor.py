import tkinter as tk
from tkinter import ttk
from views.View import View
from datetime import datetime
from models.PostMessage import PostMessage
from datetime import datetime
from models.ContractAdditionalInfo import ContractAdditionalInfo
from models.PostContract import PostContract
from controllers.UserController import UserController
from controllers.BidController import BidController
from controllers.ContractController import ContractController
from controllers.MessageController import MessageController
from views.ErrorPopup import ErrorPopup
from dateutil.relativedelta import relativedelta

class DisplayOpenBidTutor(View):
    def __init__(self, webService, user, bid):
        self.user = user
        self.bid = bid
        self.deleted = False
        super().__init__(webService)
    
    def refresh(self, window, bidsTable):
        if not self.deleted:
            # Determine currently selected rows
            currentlySelectedMessage = bidsTable.focus()
            currentlySelectedMessageId = bidsTable.item(currentlySelectedMessage)['text']

            # Empty table
            for i in bidsTable.get_children():
                bidsTable.delete(i)
            
            # Get fresh bid info from API
            self.bid = BidController.getBid(self.webService, self.bid.getId())
            messages = self.bid.getMessages()

            # Display messages on screen
            for i in range(0, len(messages)):
                message = messages[i]
                user = UserController.getUser(self.webService, message.getPoster())

                messageID = message.getId()
                bidder = user.getGivenName() + " " + user.getFamilyName() + " @" + user.getUserName()
                paymentInfo = str(message.getAdditionalInfo().getPaymentInfo().getPaymentAmount()) + " " + message.getAdditionalInfo().getPaymentInfo().getPaymentFrequency()
                lessonInfo =  str(message.getAdditionalInfo().getLessonInfo().getSession_pwk()) + " session(s) per week, " + str(message.getAdditionalInfo().getLessonInfo().getHours_pl()) + " hour(s) per session"
                freeLesson = str(message.getAdditionalInfo().getFreeLesson())
                contractLength = str(message.getAdditionalInfo().getContractLength())

                bidsTable.insert("", "end", text=messageID, values=(bidder, paymentInfo, lessonInfo, freeLesson, contractLength))
                if messageID == currentlySelectedMessageId:
                            child_id = bidsTable.get_children()[-1]
                            bidsTable.focus(child_id)
                            bidsTable.selection_set(child_id)

            # Refresh screen
            window.update()
        window.after(10000, self.refresh, window, bidsTable)

    def buyout(self, contractLength, window):
        try:
            contractLengthInt = int(contractLength)
        except:
            ErrorPopup("Please type integer for contract length in months", self.webService)
            return
        if contractLengthInt < 3:
            contractLengthInt = 3
        
        firstPartyId = self.bid.getInitiator()
        secondPartyId = self.user.getId()
        subjectId = self.bid.getSubject().getId()
        dateCreated = datetime.now().isoformat()
        expiry = datetime.now() + relativedelta(months=contractLengthInt)
        expiryDate = expiry.isoformat()
        paymentInfo = self.bid.getAdditionalInfo().getPaymentInfo()
        lessonInfo = self.bid.getAdditionalInfo().getLessonInfo()
        additionalInfo = ContractAdditionalInfo(False, False, False, self.bid.getAdditionalInfo().getMinimumCompetency(), contractLengthInt)

        newContract = PostContract(firstPartyId, secondPartyId, subjectId, dateCreated, expiryDate, paymentInfo, lessonInfo, additionalInfo)
        newContractJSONObject = newContract.toJSONObject()
        postContract = ContractController.addContract(self.webService, newContractJSONObject)

        BidController.deleteBid(self.webService, self.bid)
        self.deleted = True
        window.destroy()

    def submitOpenBid(self, rate, rateType, sessionsPerWeek, hoursPerSession, freeLesson, contractLength, window):
        try:
            contractLengthInt = int(contractLength)
        except:
            ErrorPopup("Please type integer for contract length in months", self.webService)
            return
        if contractLengthInt < 3:
            contractLengthInt = 3
        messageData = PostMessage(self.bid.getId(), self.user.getId(), ' ', rate, rateType, sessionsPerWeek, hoursPerSession, freeLesson, self.bid.getInitiator(), contractLengthInt)
        messageDataJSON = messageData.toJSONObject()

        MessageController.addMessage(self.webService, messageDataJSON)

    def createFrontend(self):
        window = tk.Toplevel()
        window.title("Open Bid")

        initiator = UserController.getUser(self.webService, self.bid.getInitiator())
        initiatorText = "Initiator: " + initiator.getGivenName() + " " + initiator.getFamilyName() + " @" + initiator.getUserName()
        initiatorLabel = tk.Label(master=window, text=initiatorText)

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
        paymentInfoLabel = tk.Label(master=window, text="Payment: " + paymentText)
        
        contractLengthBuyoutLabel = tk.Label(master=window, text="Contract length (months):")
        defaultContractLength = tk.StringVar(window)
        contractLengthBuyoutSpinbox = tk.Spinbox(master=window, values=(3, 6, 12, 24), textvariable=defaultContractLength)
        defaultContractLength.set("6")
        
        buyoutButton = tk.Button(window, text='Buyout Bid', width=25, command=lambda: self.buyout(contractLengthBuyoutSpinbox.get(), window))
        
        bidLabel = tk.Label(master=window, text="Bids")
        bidsTable = ttk.Treeview(window, height=5)

        bidsTable["columns"] = ("bidder", "paymentInfo", "lessonInfo", "freeLesson", "contractLength")

        bidsTable.heading('#0', text='bidderID')
        bidsTable.heading("bidder", text="Bidder", anchor=tk.W)
        bidsTable.heading("paymentInfo", text="paymentInfo", anchor=tk.W)
        bidsTable.heading("lessonInfo", text="lessonInfo", anchor=tk.W)
        bidsTable.heading("freeLesson", text="freeLesson", anchor=tk.W)
        bidsTable.heading("contractLength", text="contractLength", anchor=tk.W)
        
        bidsTable.column("freeLesson", width=75)
        bidsTable.column("contractLength", width=100)

        createBidLabel = tk.Label(master=window, text="Create Bid")

        rateLabel = tk.Label(master=window, text="Rate")
        rateEntry = tk.Entry(master=window, fg="black", bg="white", width=50)

        rateTypeLabel = tk.Label(master=window, text="Account Type")
        rateTypeSelection = tk.StringVar()
        rateHourRadio = tk.Radiobutton(window, text="Per Hour", variable=rateTypeSelection, value="Per hour")
        rateSessionRadio = tk.Radiobutton(window, text="Per Session", variable=rateTypeSelection, value="Per session")
        rateHourRadio.select()

        sessionsPerWeekLabel = tk.Label(master=window, text="Sessions Per Week")
        sessionsPerWeekSpinbox = tk.Spinbox(window, from_=1, to_=7)

        hoursPerSessionLabel = tk.Label(master=window, text="Hours Per Session")
        hoursPerSessionSpinbox = tk.Spinbox(window, from_=1, to_=24)

        freeLessonValue = tk.BooleanVar()
        freeLessonCheckbox = tk.Checkbutton(master=window, text = "Offer free lesson", variable=freeLessonValue)

        contractLengthLabel = tk.Label(master=window, text="Contract length (months):")
        defaultContractLength = tk.StringVar(window)
        contractLengthSpinbox = tk.Spinbox(master=window, values=(3, 6, 12, 24), textvariable=defaultContractLength)
        defaultContractLength.set("6")

        submitButton = tk.Button(window, text='Submit', width=25, command= lambda: self.submitOpenBid(float(rateEntry.get()), rateTypeSelection.get(), sessionsPerWeekSpinbox.get(), hoursPerSessionSpinbox.get(), freeLessonValue.get(), contractLengthSpinbox.get(), window))

        initiatorLabel.pack()
        dateCreatedLabel.pack()
        dateCloseDownLabel.pack()
        subjectNameLabel.pack()
        subjectDescriptionLabel.pack()
        subjectCompetencyLabel.pack()
        lessonInfoLabel.pack()
        paymentInfoLabel.pack()
        contractLengthBuyoutLabel.pack()
        contractLengthBuyoutSpinbox.pack()
        buyoutButton.pack()
        bidLabel.pack()
        bidsTable.pack()
        createBidLabel.pack()
        rateLabel.pack()
        rateEntry.pack()
        rateTypeLabel.pack()
        rateHourRadio.pack()
        rateSessionRadio.pack()
        sessionsPerWeekLabel.pack()
        sessionsPerWeekSpinbox.pack()
        hoursPerSessionLabel.pack()
        hoursPerSessionSpinbox.pack()
        freeLessonCheckbox.pack()
        contractLengthLabel.pack()
        contractLengthSpinbox.pack()
        submitButton.pack()

        window.after(500, self.refresh, window, bidsTable)
        window.mainloop()