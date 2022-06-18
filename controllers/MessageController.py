from models.Message import Message

class MessageController():
    """
    MessageController class provides methods relating to the /message routes in the API.
    All methods are static so an object does not need to be instantiated.
    """
    base = 'message/'     # Static variable of the base API route for user API calls

    @staticmethod
    def addMessage(webService, messageJSON):
        """
        Submits a new message to the server to be added.
        :param webService: Instance of the WebService object used throughout the application
        :param messageJSON: JSON object containing message data
        :return: Message object containing The API response
        """
        
        # Make API call and validate response
        response = webService.post(MessageController.base, json=messageJSON)
        webService.validate(response, 201, 'Failed to submit message')

        # Return the API response
        return Message(response.json())
        
    @staticmethod
    def deleteMessage(webService, messageID):
        """
        Deletes a message from the server
        :param webService: Instance of the WebService object used throughout the application
        :param messageID: String ID of the message to delete
        :return: The API response
        """
        
        # Make API call and validate response
        response = webService.delete(MessageController.base + messageID)
        webService.validate(response, 204, 'Failed to delete message')

        # Return the API response
        return response