from controllers.BidController import BidController
from controllers.ContractController import ContractController
import tkinter as tk
from tkinter import ttk
from views.View import View
from models.ContractAdditionalInfo import ContractAdditionalInfo
from datetime import datetime
from models.PostContract import PostContract
from models.PostMessage import PostMessage
from controllers.UserController import UserController
from controllers.MessageController import MessageController
from views.ErrorPopup import ErrorPopup
from dateutil.relativedelta import relativedelta

class DisplayCloseBidStudent(View):
    def __init__(self, webService, user, bid):
        self.user = user
        self.bid = bid
        self.deleted = False
        super().__init__(webService)

    def refresh(self, window, messagesTable):
        if not self.deleted:
            # Determine currently selected rows
            currentlySelectedMessage = messagesTable.focus()
            currentlySelectedMessageId = messagesTable.item(currentlySelectedMessage)['text']

            # Empty table
            for i in messagesTable.get_children():
                messagesTable.delete(i)

            # Get fresh bid info from API
            self.bid = BidController.getBid(self.webService, self.bid.getId())
            messages = self.bid.getMessages()

            # Display messages on screen
            for message in messages:
                senderId = message.getPoster()
                receiverId = message.getAdditionalInfo().getReceiver()

                senderObj = None
                receiverObj = None

                if senderId == self.user.getId():
                    senderObj = self.user
                    receiverObj = UserController.getUser(self.webService, receiverId)
                else:
                    receiverObj = self.user
                    senderObj = UserController.getUser(self.webService, senderId)

                messageID = message.getId()
                sender = senderObj.getGivenName() + " " + senderObj.getFamilyName() + " @" + senderObj.getUserName()
                receiver = receiverObj.getGivenName() + " " + receiverObj.getFamilyName() + " @" + receiverObj.getUserName()
                content = message.getContent()
                paymentInfo = str(message.getAdditionalInfo().getPaymentInfo().getPaymentAmount()) + " " + message.getAdditionalInfo().getPaymentInfo().getPaymentFrequency()
                lessonInfo =  str(message.getAdditionalInfo().getLessonInfo().getSession_pwk()) + " session(s) per week, " + str(message.getAdditionalInfo().getLessonInfo().getHours_pl()) + " hour(s) per session"
                freeLesson = str(message.getAdditionalInfo().getFreeLesson())
                datePosted = message.getDatePosted()
                contractLength = str(message.getAdditionalInfo().getContractLength())

                messagesTable.insert("", "end", text=messageID, values=(sender, receiver, content, paymentInfo, lessonInfo, freeLesson, datePosted, receiverObj.getId(), senderObj.getId(), contractLength))
                if messageID == currentlySelectedMessageId:
                            child_id = messagesTable.get_children()[-1]
                            messagesTable.focus(child_id)
                            messagesTable.selection_set(child_id)
            #Refresh window
            window.update()
        window.after(10000, self.refresh, window, messagesTable)

    def createFrontend(self):
        window = tk.Toplevel()
        window.title("Closed Bid")

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

        messagesLabel = tk.Label(master=window, text="Messages")
        messagesTable = ttk.Treeview(window, height=5)

        messagesTable["columns"] = ("sender", "receiver", "content", "paymentInfo", "lessonInfo", "freeLesson", "datePosted", "receiverID", "senderID", "contractLength")
        messagesTable['show'] = 'headings'
        messagesTable["displaycolumns"]=("sender", "receiver", "content", "paymentInfo", "lessonInfo", "freeLesson", "datePosted", "contractLength")

        messagesTable.heading('#0', text='messageID')
        messagesTable.heading("sender", text="Sender", anchor=tk.W)
        messagesTable.heading("receiver", text="Receiver", anchor=tk.W)
        messagesTable.heading("content", text="Content", anchor=tk.W)
        messagesTable.heading("paymentInfo", text="paymentInfo", anchor=tk.W)
        messagesTable.heading("lessonInfo", text="lessonInfo", anchor=tk.W)
        messagesTable.heading("freeLesson", text="freeLesson", anchor=tk.W)
        messagesTable.heading("datePosted", text="datePosted", anchor=tk.W)
        messagesTable.heading('receiverID', text='receiverID', anchor=tk.W)
        messagesTable.heading('senderID', text='senderID', anchor=tk.W)
        messagesTable.heading('contractLength', text='contractLength', anchor=tk.W)

        messagesTable.column("freeLesson", width=75)
        messagesTable.column("contractLength", width=100)

        contractLengthWinnerLabel = tk.Label(master=window, text="Contract length (months):")
        defaultContractLength = tk.StringVar(window)
        contractLengthWinnerSpinbox = tk.Spinbox(master=window, values=(3, 6, 12, 24), textvariable=defaultContractLength)
        defaultContractLength.set("6")

        # Select winner button
        selectWinnerButton = tk.Button(window, text='Select winner', width=25, command= lambda: self.selectWinner(messagesTable, contractLengthWinnerSpinbox.get(), window))

        createBidLabel = tk.Label(master=window, text="Send Reply (select a message above)")

        contentLabel = tk.Label(master=window, text="Content")
        contentEntry = tk.Entry(master=window, fg="black", bg="white", width=50)

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

        submitButton = tk.Button(window, text='Submit', width=25, command= lambda: self.submitReply(contentEntry.get(), float(rateEntry.get()), rateTypeSelection.get(), sessionsPerWeekSpinbox.get(), hoursPerSessionSpinbox.get(), freeLessonValue.get(), messagesTable, contractLengthSpinbox.get(), window))

        dateCreatedLabel.pack()
        dateCloseDownLabel.pack()
        subjectNameLabel.pack()
        subjectDescriptionLabel.pack()
        subjectCompetencyLabel.pack()
        lessonInfoLabel.pack()
        paymentInfoLabel.pack()
        messagesLabel.pack()
        messagesTable.pack()
        contractLengthWinnerLabel.pack()
        contractLengthWinnerSpinbox.pack()
        selectWinnerButton.pack()
        createBidLabel.pack()
        contentLabel.pack()
        contentEntry.pack()
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

        window.after(500, self.refresh, window, messagesTable)
        window.mainloop()
    
    def submitReply(self, content, rate, rateType, sessionsPerWeek, hoursPerSession, freeLesson, messagesTable, contractLength, window):
        receiver = messagesTable.item(messagesTable.focus())['values'][8]
        if receiver == self.user.getId():
            return
        
        try:
            contractLengthInt = int(contractLength)
        except:
            ErrorPopup("Please type integer for contract length in months", self.webService)
            return
        if contractLengthInt < 3:
            contractLengthInt = 3
            
        messageData = PostMessage(self.bid.getId(), self.user.getId(), content, rate, rateType, sessionsPerWeek, hoursPerSession, freeLesson, receiver, contractLengthInt)
        messageDataJSON = messageData.toJSONObject()

        MessageController.addMessage(self.webService, messageDataJSON)
        
    def selectWinner(self, messagesTable, studentContractLength, window):
        messageId = messagesTable.item(messagesTable.focus())['text']
        receiver = messagesTable.item(messagesTable.focus())['values'][8]

        if receiver == self.user.getId():
            return
        
        try:
            contractLengthInt = int(studentContractLength)
        except:
            ErrorPopup("Please type integer for contract length in months", self.webService)
            return
        if contractLengthInt < 3:
            contractLengthInt = 3

        message = None
        messages = self.bid.getMessages()
        for i in range(0, len(messages)):
            if messages[i].getId() == messageId:
                message = messages[i]
                break

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