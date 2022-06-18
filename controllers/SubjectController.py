from models.Subject import Subject

class SubjectController():
    """
    BidController class provides methods relating to the /bid routes in the API.
    All methods are static so an object does not need to be instantiated.
    """
    base = 'subject/'     # Static variable of the base API route for user API calls

    @staticmethod
    def getSubjects(webService):
        """
        Get all subjects currently in the system as an array of Subject objects.
        :param webService: Instance of the WebService object used throughout the application
        :return: Array of Subject objects containing the API response
        """
        
        # Make API call and validate response
        response = webService.get(SubjectController.base)
        webService.validate(response, 200, 'Failed to get subjects')

        # Instantiate Subject objects from response
        responseJSON = response.json()
        subjects = []

        for subject in responseJSON:
            subjects.append(Subject(subject))

        # Return the API response
        return subjects