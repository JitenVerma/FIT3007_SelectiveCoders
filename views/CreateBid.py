from controllers.BidController import BidController
import tkinter as tk
from views.View import View
from models.LessonInfo import LessonInfo
from models.PaymentInfo import PaymentInfo
from models.BidAdditionalInfo import BidAdditionalInfo
from models.PostBid import PostBid
from datetime import datetime
from datetime import timedelta
from controllers.SubjectController import SubjectController

class CreateBid(View):
    """
    Creates the CreateBid view where students can create a new bid.
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
        super().__init__(webService)
    
    def postBid(self, bidType, competency, subject, hoursPerLesson, lessonsPerWeek, preferredRate, paymentFrequency, window):
        """
        Submits the new bid to the server and then closes the window.
        :param bidType: String (either open or closed) to denote the bid type
        :param competency: Int of the required competency level
        :param subject: String of the required subject (name - description #ID)
        :param hoursPerLesson: Int of hours per lesson
        :param lessonsPerWeek: Int of lessons per week
        :param preferredRate: Float of rate
        :param paymentFrequency: String (either Per hour or Per session) to denote payment frequency
        :param window: Tk window object currently used
        :return: None
        """
        
        # Determine studentID and subjectID
        studentID = self.user.getId()
        subjectID = subject.split('#')[1]

        # Adding date created
        currentTime = datetime.now()
        bidCreatedTime = currentTime.isoformat()

        # Adding date closed down
        if bidType == 'open':
            closedDownTime = currentTime + timedelta(minutes=30)
            bidClosedDownTime = closedDownTime.isoformat()
        elif bidType == 'closed':
            closedDownTime = currentTime + timedelta(weeks=1)
            bidClosedDownTime = closedDownTime.isoformat()

        # Adding additional info
        lessonInfo = LessonInfo({'session_pwk': lessonsPerWeek, 'hours_pl': hoursPerLesson})
        paymentInfo = PaymentInfo({'paymentAmount': preferredRate, 'paymentFrequency': paymentFrequency})
        bidAdditionalInfo = BidAdditionalInfo(competency, lessonInfo, paymentInfo)

        # Create new post bid object and submit it to the server
        newPostBid = PostBid(bidType, studentID, bidCreatedTime, subjectID, bidAdditionalInfo)
        newPostBidJSON = newPostBid.toJSONObject()
        postedBid = BidController.createBid(self.webService, newPostBidJSON)
        
        # Set the close date for the bid
        BidController.setBidCloseDown(self.webService, postedBid.getId(), bidClosedDownTime)
        
        # Close the current window and to go back to homepage
        window.destroy()

    def createFrontend(self):
        """
        Create the frontend of the CreateBid view
        :return: None
        """
        
        # Instantiate window to be used
        window = tk.Tk()
        window.title('Tutoring system')
        bidLabel = tk.Label(window, text="Bid")

        # Decide between open/closed bid
        bidType = tk.StringVar(window)
        openRadioButton = tk.Radiobutton(window, text='Open', variable=bidType, value="open")
        closedRadioButton = tk.Radiobutton(window, text='Closed', variable=bidType, value="closed")
        openRadioButton.select()
        
        # Decide required competency level
        requiredCompetencyLevelLabel = tk.Label(window, text="Competency level required:")
        competencyLevelSpinbox = tk.Spinbox(window, from_=1, to_=10)

        # Decide the subject
        subjectLabel = tk.Label(window, text="Select the subject required:")
        subjectListbox = tk.Listbox(window)

        # Add subjects to ListBox
        subjects = SubjectController.getSubjects(self.webService)       # Get all subjects from API
        for subject in subjects:
            subjectListbox.insert(tk.END, subject.getName() + ' - ' + subject.getDescription() + ' #' + subject.getId())
        
        # Decide hours per lesson required
        hoursPerLessonLabel = tk.Label(window, text="Length of lessons required (Hours):")
        hoursPerLessonSpinbox = tk.Spinbox(window, from_=1, to_=24)

        # Decide lessons per week
        lessonsPerWeekLabel = tk.Label(window, text="Lessons per week required:")
        lessonsPerWeekSpinbox = tk.Spinbox(window, from_=1, to_=7)

        # Decide preferred rate
        preferredRateLabel = tk.Label(window, text="Preferred rate:")
        preferredRateEntry = tk.Entry(window, fg="black", bg="white", width=50)

        # Decide whether preferred rate is per hour or per session
        paymentFrequency = tk.StringVar(window)
        hourRadio = tk.Radiobutton(window, text='Per hour', variable=paymentFrequency, value="Per hour")
        sessionRadio = tk.Radiobutton(window, text='Per session', variable=paymentFrequency, value="Per session")       
        hourRadio.select()

        # Post Bid button
        postBiddingButton = tk.Button(window, text='Post Bid', width=25, command= lambda: self.postBid(bidType.get(), competencyLevelSpinbox.get(), subjectListbox.get(subjectListbox.curselection()), hoursPerLessonSpinbox.get(), lessonsPerWeekSpinbox.get(), preferredRateEntry.get(), paymentFrequency.get(), window))

        # Pack elements onto window       
        bidLabel.pack()
        openRadioButton.pack()
        closedRadioButton.pack()
        requiredCompetencyLevelLabel.pack()
        competencyLevelSpinbox.pack()
        subjectLabel.pack()
        subjectListbox.pack()
        hoursPerLessonLabel.pack()
        hoursPerLessonSpinbox.pack()
        lessonsPerWeekLabel.pack()
        lessonsPerWeekSpinbox.pack()
        preferredRateLabel.pack()
        preferredRateEntry.pack()
        hourRadio.pack()
        sessionRadio.pack()
        postBiddingButton.pack()

        # Start the window mainloop
        window.mainloop()