import tkinter as tk
from tkinter import ttk
from datetime import datetime
from views.DisplayOpenBidTutor import DisplayOpenBidTutor
from views.DisplayCloseBidTutor import DisplayCloseBidTutor
from views.ViewContract import ViewContract
from views.MonitoringPage import MonitoringPage
from views.View import View
from controllers.UserController import UserController
from controllers.ContractController import ContractController
from controllers.BidController import BidController
from views.ErrorPopup import ErrorPopup
from dateutil.relativedelta import relativedelta

class TutorHomePage(View):
    """
    Creates the TutorHomePage view where tutors can manage their bids and contracts.
    Extends the View class
    """

    def __init__(self, webService, user):
        """
        Constructor initialises some variables and runs the super constructor (which runs createFrontend)
        :param webService: Instance of the WebService object used throughout the application
        :param user: User object of the logged in user
        :return: None
        """

        self.user = user
        self.bids = []
        self.contracts = []
        super().__init__(webService)
    
    def refresh(self, window, contractsTable, bidsTable, firstIteration):
        """
        Refreshes all data displayed on the view by repopulating the value of variables.
        :param window: Tk instance of window to refresh data on
        :return: None
        """

        # Reset variables
        self.user = UserController.getUser(self.webService, self.user.getId())      # Get fresh user data from API
        self.bids = []
        self.contracts = []

        # Determine currently selected rows
        currentlySelectedContract = contractsTable.focus()
        currentlySelectedContractId = contractsTable.item(currentlySelectedContract)['text']

        currentlySelectedBid = bidsTable.focus()
        currentlySelectedBidId = bidsTable.item(currentlySelectedBid)['text']
        
        # Empty tables
        for i in contractsTable.get_children():
            contractsTable.delete(i)
        for i in bidsTable.get_children():
            bidsTable.delete(i)

        # Get all contracts from API
        contracts = ContractController.getContracts(self.webService)
        expiringContracts = []

        # Filter contracts to display only those related to the tutor
        for contract in contracts:
            if contract.getSecondParty().getId() == self.user.getId():
                self.contracts.append(contract)

                contractID = contract.getId()
                otherParty = contract.getFirstParty().getGivenName() + " " + contract.getFirstParty().getFamilyName() + " @" + contract.getFirstParty().getUserName()
                subject = contract.getSubject().getName() + " " + contract.getSubject().getDescription()

                expired = "False"
                if (datetime.now()) >  datetime.strptime(contract.getExpiryDate(), "%Y-%m-%dT%H:%M:%S.%fZ"):
                    expired = "True"

                contractsTable.insert("", "end", text=contractID, values=(otherParty, subject, expired))
                if contractID == currentlySelectedContractId:
                    child_id = contractsTable.get_children()[-1]
                    contractsTable.focus(child_id)
                    contractsTable.selection_set(child_id)
                if firstIteration:
                    if (datetime.now()) <  datetime.strptime(contract.getExpiryDate(), "%Y-%m-%dT%H:%M:%S.%fZ"):
                        if (datetime.now() + relativedelta(months=1)) >  datetime.strptime(contract.getExpiryDate(), "%Y-%m-%dT%H:%M:%S.%fZ"):
                            expiringContracts.append(contractID)

        # Get all bids from API
        bids = BidController.getBids(self.webService)

        # Filter bids to only show relevant ones (eg not closed and user is competent)
        currentTime = datetime.now()
        for bid in bids:
            if (bid.getDateClosedDown() is None) or (currentTime < datetime.strptime(bid.getDateClosedDown(), "%Y-%m-%dT%H:%M:%S.%fZ")):
                competent = False
                for competency in self.user.getCompetencies():
                    if bid.getSubject().getId() == competency.getSubject():
                        if int(bid.getAdditionalInfo().getMinimumCompetency()) + 2 <= competency.getLevel():
                            competent = True
                            break
                
                if not competent:
                    continue
                
                self.bids.append(bid)

                # Get student information from API
                student = UserController.getUser(self.webService, bid.getInitiator())

                bidID = bid.getId()
                otherParty = student.getGivenName() + " " + student.getFamilyName() + " @" + student.getUserName()
                type = bid.getType()
                subject = bid.getSubject().getName() + " " + bid.getSubject().getDescription()

                bidsTable.insert("", "end", text=bidID, values=(otherParty, type, subject))
                if bidID == currentlySelectedBidId:
                        child_id = bidsTable.get_children()[-1]
                        bidsTable.focus(child_id)
                        bidsTable.selection_set(child_id)

        # Verify that the JWT is still valid and refresh the window
        UserController.verifyJWT(self.webService)       # Verify that the JWT is still valid
        window.update()

        # Recursive call to continuously refresh
        window.after(10000, self.refresh, window, contractsTable, bidsTable, False)

        if firstIteration and len(expiringContracts) > 0:
            finalExpiringContacts = "\n".join(expiringContracts)
            ErrorPopup("You have less than 1 month remaining until the following contract expires: \nContract IDs:\n" + finalExpiringContacts, self.webService)

    def createFrontend(self):
        """
        Create the frontend of the TutorHomePage view
        :return: None
        """

        # Instantiate window to be used
        window = tk.Tk()
        window.title("Tutor Homepage")

        # Add UI elements
        subscribeButton = tk.Button(window, text='Subscribe', width=25, command= lambda: self.subscribeButtonClick(bidsTable.item(bidsTable.focus())['text'], bidsTable.item(bidsTable.focus())['values'][1]))
        monitorPageButton = tk.Button(window, text='Open Monitoring Page', width=25, command= lambda: self.monitoringPageButtonClick())

        # Display current contracts
        nameLabel = tk.Label(text = self.user.getGivenName() + " " + self.user.getFamilyName() + " @" + self.user.getUserName())
        contractsLabel = tk.Label(text="Contracts")

        # Create table for displaying contracts
        contractsTable = ttk.Treeview(window)
        contractsTable.bind("<Double-1>", self.handleContractClick)

        contractsTable["columns"] = ("otherParty", "subject", "expired")
        contractsTable.column("otherParty", width=200, minwidth=100, stretch=tk.YES)
        contractsTable.column("subject", width=200, minwidth=10, stretch=tk.YES)
        contractsTable.column("expired", width=200, minwidth=10, stretch=tk.YES)

        contractsTable.heading('#0', text='ID')
        contractsTable.heading("otherParty", text="otherParty", anchor=tk.W)
        contractsTable.heading("subject", text="subject", anchor=tk.W)
        contractsTable.heading("expired", text="expired", anchor=tk.W)
        
        # Display currently open bids
        bidLabel = tk.Label(text="Bids")

        # Create table to show bids
        bidsTable = ttk.Treeview(window)
        bidsTable.bind("<Double-1>", self.handleBidClick)

        bidsTable["columns"] = ("otherParty", "type", "subject")
        bidsTable.column("otherParty", width=200, minwidth=100, stretch=tk.YES)
        bidsTable.column("subject", width=200, minwidth=10, stretch=tk.YES)

        bidsTable.heading('#0', text='ID')
        bidsTable.heading("otherParty", text="otherParty", anchor=tk.W)
        bidsTable.heading("type", text="type", anchor=tk.W)
        bidsTable.heading("subject", text="subject", anchor=tk.W)

        refreshButton = tk.Button(window, text='Refresh', width=25, command= lambda: self.refresh(window, contractsTable, bidsTable, False))

        # Pack elements onto window
        nameLabel.pack()
        refreshButton.pack()
        contractsLabel.pack()
        contractsTable.pack(side=tk.TOP, fill=tk.X)
        bidLabel.pack()
        bidsTable.pack(side=tk.TOP, fill=tk.X)
        subscribeButton.pack()
        monitorPageButton.pack()

        firstIteration = True

        # Refresh the page
        window.after(500, self.refresh, window, contractsTable, bidsTable, firstIteration)

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
                elif bid.getType() == 'closed':
                    DisplayCloseBidTutor(self.webService, self.user, bid)
                    break
    
    def handleContractClick(self, event):
        """
        Runs when user selects a contract from the table and displays information about that contract
        :param event: Tk event with information about the selection
        :return: None
        """

        # Extract selected contract ID from the event
        selectedRow = event.widget.selection()[0]
        contractId = event.widget.item(selectedRow, "text")

        # Find the contract and display information
        for contract in self.contracts:
            if contract.getId() == contractId:
                ViewContract(self.webService, self.user, contract)
                break

    def subscribeButtonClick(self, selectedBidId, bidType):
        if bidType == 'closed':
            ErrorPopup("You can only subscribe to open bids", self.webService)
            return

        if selectedBidId == "":
            ErrorPopup("Please select a bid to subscribe to", self.webService)
            return

        UserController.addSubscribedBid(self.webService, self.user, selectedBidId)
        self.user = UserController.getUser(self.webService, self.user.getId())
            
    def monitoringPageButtonClick(self):
        MonitoringPage(self.webService, self.user)