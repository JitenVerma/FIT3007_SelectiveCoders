import tkinter as tk
from tkinter import ttk
from views.View import View
from models.PostMessage import PostMessage
from controllers.MessageController import MessageController
from controllers.UserController import UserController
from controllers.BidController import BidController
from views.ErrorPopup import ErrorPopup

class DisplayCloseBidTutor(View):
    def __init__(self, webService, user, bid):
        self.user = user
        self.bid = bid
        super().__init__(webService)
    
    def refresh(self, window, initiator, messagesTable):
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
        for i in range(0, len(messages)):
            message = messages[i]

            if message.getAdditionalInfo().getReceiver() == self.user.getId() or message.getPoster() == self.user.getId():
                senderObj = self.user
                receiverObj = initiator
                if message.getPoster() != self.user.getId():
                    senderObj = initiator
                    receiverObj = self.user

                messageID = message.getId()
                sender = senderObj.getGivenName() + " " + senderObj.getFamilyName() + " @" + senderObj.getUserName()
                receiver = receiverObj.getGivenName() + " " + receiverObj.getFamilyName() + " @" + receiverObj.getUserName()
                content = message.getContent()
                paymentInfo = str(message.getAdditionalInfo().getPaymentInfo().getPaymentAmount()) + " " + message.getAdditionalInfo().getPaymentInfo().getPaymentFrequency()
                lessonInfo =  str(message.getAdditionalInfo().getLessonInfo().getSession_pwk()) + " session(s) per week, " + str(message.getAdditionalInfo().getLessonInfo().getHours_pl()) + " hour(s) per session"
                freeLesson = str(message.getAdditionalInfo().getFreeLesson())
                datePosted = message.getDatePosted()
                contractLength = str(message.getAdditionalInfo().getContractLength())

                messagesTable.insert("", "end", text=messageID, values=(sender, receiver, content, paymentInfo, lessonInfo, freeLesson, datePosted, contractLength))
                if messageID == currentlySelectedMessageId:
                        child_id = messagesTable.get_children()[-1]
                        messagesTable.focus(child_id)
                        messagesTable.selection_set(child_id)
        
        #Refresh window
        window.update()
        window.after(10000, self.refresh, window, initiator, messagesTable)

    def submitClosedBid(self, content, rate, rateType, sessionsPerWeek, hoursPerSession, freeLesson, contractLength, window):
        try:
            contractLengthInt = int(contractLength)
        except:
            ErrorPopup("Please type integer for contract length in months", self.webService)
            return
        if contractLengthInt < 3:
            contractLengthInt = 3
            
        messageData = PostMessage(self.bid.getId(), self.user.getId(), content, rate, rateType, sessionsPerWeek, hoursPerSession, freeLesson, self.bid.getInitiator(), contractLengthInt)
        messageDataJSON = messageData.toJSONObject()

        MessageController.addMessage(self.webService, messageDataJSON)

    def createFrontend(self):
        window = tk.Toplevel()
        window.title("Closed Bid")

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

        messagesLabel = tk.Label(master=window, text="Messages")
        messagesTable = ttk.Treeview(window, height=5)

        messagesTable["columns"] = ("sender", "receiver", "content", "paymentInfo", "lessonInfo", "freeLesson", "datePosted", "contractLength")
        messagesTable['show'] = 'headings'

        messagesTable.heading('#0', text='messageID')
        messagesTable.heading("sender", text="Sender", anchor=tk.W)
        messagesTable.heading("receiver", text="Receiver", anchor=tk.W)
        messagesTable.heading("content", text="Content", anchor=tk.W)
        messagesTable.heading("paymentInfo", text="paymentInfo", anchor=tk.W)
        messagesTable.heading("lessonInfo", text="lessonInfo", anchor=tk.W)
        messagesTable.heading("freeLesson", text="freeLesson", anchor=tk.W)
        messagesTable.heading("datePosted", text="datePosted", anchor=tk.W)
        messagesTable.heading("contractLength", text="contractLength", anchor=tk.W)

        messagesTable.column("freeLesson", width=75)
        messagesTable.column("contractLength", width=100)

        createBidLabel = tk.Label(master=window, text="Send Message")

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
        contractLengthSpinbox = tk.Spinbox(master=window, values=(3, 6, 12, 24))
        defaultContractLength.set("6")

        submitButton = tk.Button(window, text='Submit', width=25, command= lambda: self.submitClosedBid(contentEntry.get(), float(rateEntry.get()), rateTypeSelection.get(), sessionsPerWeekSpinbox.get(), hoursPerSessionSpinbox.get(), freeLessonValue.get(), contractLengthSpinbox.get(),window))

        initiatorLabel.pack()
        dateCreatedLabel.pack()
        dateCloseDownLabel.pack()
        subjectNameLabel.pack()
        subjectDescriptionLabel.pack()
        subjectCompetencyLabel.pack()
        lessonInfoLabel.pack()
        paymentInfoLabel.pack()
        messagesLabel.pack()
        messagesTable.pack()
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

        window.after(500, self.refresh, window, initiator, messagesTable)
        window.mainloop()