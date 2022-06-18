from models.User import User
from views.ErrorPopup import ErrorPopup

class UserController():
    """
    UserController class provides methods relating to the /user routes in the API.
    All methods are static so an object does not need to be instantiated.
    """
    base = 'user/'     # Static variable of the base API route for user API calls

    @staticmethod
    def loginUser(webService, username, password):
        """
        Login the user with provided credentials, and store the returned jwt in the webService instance.
        :param webService: Instance of the WebService object used throughout the application
        :param username: string of the username of the user to login
        :param password: string of the password to login with
        :return: JSON object containing the API response
        """

        # Make API call and validate response
        response = webService.post(UserController.base + 'login', { 'userName': username, 'password': password }, { 'jwt': 'true' })
        webService.validate(response, 200, 'Login failed')

        # Store the JWT in the webService for later use
        responseJSON = response.json()
        encodedJWT = responseJSON['jwt']
        webService.setJWT(encodedJWT)

        # Return the API response
        return responseJSON
    
    @staticmethod
    def getUser(webService, userID):
        """
        Query the API for a specific userID and return a User object
        :param webService: Instance of the WebService object used throughout the application
        :param userID: string of the userID of the user whose info should be retrieved
        :return: User object with the API response data
        """

        # Make API call and validate response
        response = webService.get(UserController.base + userID, {'fields': 'competencies.subject'})
        webService.validate(response, 200, 'Failed to get user information')

        # Return the API response
        return User(response.json())

    @staticmethod
    def updateUser(webService, userID, data):
        """
        Partially update a user (patch) with the provided data
        :param webService: Instance of the WebService object used throughout the application
        :param userID: string of the userID of the user to update
        :param data: JSON object of updated user data
        :return: The API response data
        """

        # Make API call and validate response
        response = webService.patch(UserController.base + userID, json=data)
        webService.validate(response, 200, 'Failed to update user information')

        # Return the API response
        return response.json()
    
    @staticmethod
    def addSubscribedBid(webService, user, bidID):
        """
        Subscribe the user to a bid
        :param webService: Instance of the WebService object used throughout the application
        :param user: User object of the current user
        :param bidID: String ID of the bid to subscribe to
        :return: The API response data
        """

        # Get currently subscribed bids
        data = { 'additionalInfo': user.getAdditionalInfo().toJSON() }

        # Check that the new bid is unique
        for bid in data['additionalInfo']['subscribedBids']:
            if bid == bidID:
                errorMessage = 'You are already subscribed to this bid'
                ErrorPopup(errorMessage, webService)
                raise Exception(errorMessage)

        # Add the new bid to the list
        data['additionalInfo']['subscribedBids'].append(bidID)

        # Make API call and validate response
        return UserController.updateUser(webService, user.getId(), data)
    
    @staticmethod
    def unsubscribeBid(webService, user, bidID):
        """
        Unsubscribes the user from a bid
        :param webService: Instance of the WebService object used throughout the application
        :param user: User object of the current user
        :param bidID: String ID of the bid to unsubscribe to
        :return: The API response data
        """

        # Get currently subscribed bids
        data = { 'additionalInfo': user.getAdditionalInfo().toJSON() }

        # Remove the bid
        try:
            data['additionalInfo']['subscribedBids'].remove(bidID)
        except:
            errorMessage = 'Not subscribed to bid which you are trying to unsubscribe from'
            ErrorPopup(errorMessage, webService)
            raise Exception(errorMessage)

        # Make API call and validate response
        return UserController.updateUser(webService, user.getId(), data)
    
    @staticmethod
    def verifyJWT(webService):
        response = webService.post(UserController.base + 'verify-token', {'jwt': webService.getJWT()}, {}, False)
        webService.validate(response, 200, 'Your login has expired. Please reopen the app and login again.')