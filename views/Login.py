import tkinter as tk
from views.View import View
import jwt
from views.StudentHomePage import StudentHomePage
from views.TutorHomePage import TutorHomePage
from views.ErrorPopup import ErrorPopup
from controllers.UserController import UserController

class Login(View):
    """
    Creates the Login view where users can login as either a student or tutor.
    Extends the View class
    """
    
    def __init__(self, webService):
        """
        Constructor just calls the super constructor of the main View class
        :param webService: Instance of the WebService object used throughout the application
        :return: None
        """
        super().__init__(webService)        # Call the parent constructor

    def onLogin(self, username, password, userType, window):
        """
        onLogin function handles the login button click and attempts to login the user
        :param username: string of the username of the user to login
        :param password: string of the password to login with
        :param userType: string (either student or tutor) explaining what the user wants to login as
        :param window: Tk object of the current window
        :return: None
        """

        # Attempt to login the user with the provided credentials
        loginResponse = UserController.loginUser(self.webService, username, password)

        # Decode the jwt and extract the user ID
        decodedJWT = jwt.decode(loginResponse['jwt'], options={"verify_signature": False})
        userID = decodedJWT['sub']

        # Make another API call to get further user info as a User object
        user = UserController.getUser(self.webService, userID)

        # Check the user actually matches the userType they requested, and if so, open the homepage
        if userType == 'student':
            if user.getIsStudent():
                window.destroy()
                StudentHomePage(self.webService, user)
            else:
                ErrorPopup('This user is not a student', self.webService)
        elif userType == 'tutor':
            if user.getIsTutor():
                window.destroy()
                TutorHomePage(self.webService, user)
            else:
                ErrorPopup('This user is not a tutor', self.webService)
    
    def createFrontend(self):
        """
        Create the frontend of the Login view
        :return: None
        """

        # Instantiate window to be used
        window = tk.Tk()
        window.title('Tutoring system')

        # Add UI elements
        usernameLabel = tk.Label(text="Username")
        usernameEntry = tk.Entry(fg="black", bg="white", width=50)

        passwordLabel = tk.Label(text="Password")
        passwordEntry = tk.Entry(fg="black", bg="white", width=50)

        loginButton = tk.Button(window, text='Login', width=25, command= lambda: self.onLogin(usernameEntry.get(), passwordEntry.get(), typeSelection.get(), window))

        typeLabel = tk.Label(text="Account Type")
        typeSelection = tk.StringVar()
        typeStudentRadio = tk.Radiobutton(window, text="Student", variable=typeSelection, value="student")
        typeTutorRadio = tk.Radiobutton(window, text="Tutor", variable=typeSelection, value="tutor")
        typeStudentRadio.select()

        # Pack elements onto window
        usernameLabel.pack()
        usernameEntry.pack()
        passwordLabel.pack()
        passwordEntry.pack()
        typeLabel.pack()
        typeStudentRadio.pack()
        typeTutorRadio.pack()
        loginButton.pack()

        # Start the window mainloop
        window.mainloop()