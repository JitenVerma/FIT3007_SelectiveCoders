import tkinter as tk
from tkinter import ttk
from datetime import datetime
from views.View import View
from controllers.UserController import UserController
from controllers.BidController import BidController
from views.DisplayOpenBidTutor import DisplayOpenBidTutor

class MonitoringPage(View):
    def __init__(self, webService, user):
        self.user = user
        self.bidIds = []
        self.bids = []
        super().__init__(webService)
    
    def refresh(self, window, bidsTable):
        # Determine currently selected rows
        currentlySelectedBid = bidsTable.focus()
        currentlySelectedBidId = bidsTable.item(currentlySelectedBid)['text']
        
        # Empty table
        for i in bidsTable.get_children():
            bidsTable.delete(i)

        # Update user
        self.user = UserController.getUser(self.webService, self.user.getId())

        # Update bidIds for the subscibed bids
        self.bidIds = self.user.getAdditionalInfo().getSubscribedBids()

        # Reset bids
        self.bids = []

        for bidId in self.bidIds:
            try:
                self.bids.append(BidController.getBid(self.webService, bidId, True))
            except:
                self.unsubscribe(bidId)

        # Filter bids to only show relevant ones (eg not closed and user is competent)
        currentTime = datetime.now()
        for bid in self.bids:
            if (bid.getDateClosedDown() is None) or (currentTime < datetime.strptime(bid.getDateClosedDown(), "%Y-%m-%dT%H:%M:%S.%fZ")):
                competent = False
                for competency in self.user.getCompetencies():
                    if bid.getSubject().getId() == competency.getSubject():
                        if int(bid.getAdditionalInfo().getMinimumCompetency()) + 2 <= competency.getLevel():
                            competent = True
                            break
                
                if not competent:
                    continue
                
                #self.bids.append(bid)

                # Get student information from API
                student = UserController.getUser(self.webService, bid.getInitiator())

                bidID = bid.getId()
                otherParty = student.getGivenName() + " " + student.getFamilyName() + " @" + student.getUserName()
                type = bid.getType()
                subject = bid.getSubject().getName() + " " + bid.getSubject().getDescription()

                bidsTable.insert("", "end", text=bidID, values=(otherParty, type, subject, "", "", "", ""))
                if bidID == currentlySelectedBidId:
                        child_id = bidsTable.get_children()[-1]
                        bidsTable.focus(child_id)
                        bidsTable.selection_set(child_id)
                
                # Obtain parent ID for tree element
                child_id = bidsTable.get_children()[-1]
                parent_id = bidsTable.parent(child_id)

                messages = bid.getMessages()
                # Display messages on screen
                for i in range(0, len(messages)):
                    message = messages[i]
                    user = UserController.getUser(self.webService, message.getPoster())

                    messageID = message.getId()
                    bidder = user.getGivenName() + " " + user.getFamilyName() + " @" + user.getUserName()
                    paymentInfo = str(message.getAdditionalInfo().getPaymentInfo().getPaymentAmount()) + " " + message.getAdditionalInfo().getPaymentInfo().getPaymentFrequency()
                    lessonInfo =  str(message.getAdditionalInfo().getLessonInfo().getSession_pwk()) + " session(s) per week, " + str(message.getAdditionalInfo().getLessonInfo().getHours_pl()) + " hour(s) per session"
                    freeLesson = str(message.getAdditionalInfo().getFreeLesson())

                    bidsTable.insert(parent_id, "end", text=bidID, values=("", "", "", bidder, paymentInfo, lessonInfo, freeLesson))

        window.update()
        window.after(10000, self.refresh, window, bidsTable)

    def createFrontend(self):
        # Instantiate window to be used
        window = tk.Toplevel()
        window.title("Monitoring Page")

        # Display currently open bids
        bidLabel = tk.Label(window, text="Bids")

        # Create table to show bids
        bidsTable = ttk.Treeview(window, height=10)
        bidsTable.bind("<Double-1>", self.handleBidClick)

        bidsTable["columns"] = ("otherParty", "type", "subject", "bidder", "paymentInfo", "lessonInfo", "freeLesson")
        bidsTable.column("otherParty", width=200, minwidth=100, stretch=tk.YES)
        bidsTable.column("subject", width=200, minwidth=10, stretch=tk.YES)
        
        bidsTable.heading('#0', text='ID')
        bidsTable.heading("otherParty", text="otherParty", anchor=tk.W)
        bidsTable.heading("type", text="type", anchor=tk.W)
        bidsTable.heading("subject", text="subject", anchor=tk.W)
        bidsTable.heading("bidder", text="Bidder", anchor=tk.W)
        bidsTable.heading("paymentInfo", text="paymentInfo", anchor=tk.W)
        bidsTable.heading("lessonInfo", text="lessonInfo", anchor=tk.W)
        bidsTable.heading("freeLesson", text="freeLesson", anchor=tk.W)
        bidsTable['show'] = 'headings'      # Hide the first ID column

        bidsTable.column("freeLesson", width=75)

        refreshButton = tk.Button(window, text='Refresh', width=25, command= lambda: self.refresh(window, bidsTable))
        unsubscribeButton = tk.Button(window, text='Unsubscribe', width=25, command= lambda: self.unsubscribe(bidsTable.item(bidsTable.focus())['text']))
        
        # Packing objects for viewing
        refreshButton.pack()
        bidLabel.pack()
        bidsTable.pack()
        unsubscribeButton.pack()

        # Refresh the page
        window.after(500, self.refresh, window, bidsTable)

        # Start the window mainloop
        window.mainloop()

    def handleBidClick(self, event):
        """
        Runs when user selects a bid from the table and displays information about that bid
        :param event: Tk event with information about the selection
        :return: None
        """

        # Extract selected bid ID from the event
        selectedRow = event.widget.selection()[0]
        bidID = event.widget.item(selectedRow, "text")

        # Find the bid and display information
        for bid in self.bids:
            if bid.getId() == bidID:
                if bid.getType() == 'open':
                    DisplayOpenBidTutor(self.webService, self.user, bid)
                    break
    
    def unsubscribe(self, bidID):
        if bidID != '':
            UserController.unsubscribeBid(self.webService, self.user, bidID)