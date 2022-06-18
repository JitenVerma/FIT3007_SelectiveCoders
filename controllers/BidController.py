from models.Bid import Bid
from controllers.MessageController import MessageController

class BidController():
    """
    BidController class provides methods relating to the /bid routes in the API.
    All methods are static so an object does not need to be instantiated.
    """
    base = 'bid/'     # Static variable of the base API route for user API calls

    @staticmethod
    def getBids(webService):
        """
        Get all bids currently in the system as an array of Bid objects.
        :param webService: Instance of the WebService object used throughout the application
        :return: Array of Bid objects containing the API response
        """
        
        # Make API call and validate response
        response = webService.get(BidController.base, {'fields': 'messages'})
        webService.validate(response, 200, 'Failed to get bids')

        # Instantiate Bid objects from response
        responseJSON = response.json()
        bids = []

        for bid in responseJSON:
            bids.append(Bid(bid))

        # Return the API response
        return bids
    
    @staticmethod
    def getBid(webService, bidID, noPopup = False):
        """
        Get a specific bid by it's ID.
        :param webService: Instance of the WebService object used throughout the application
        :param bidID: String ID of the bid to get
        :return: Bid object containing the API response
        """
        
        # Make API call and validate response
        response = webService.get(BidController.base + bidID, {'fields': 'messages'})
        webService.validate(response, 200, 'Failed to get bid', noPopup)
        
        # Return the API response
        return Bid(response.json())
    
    @staticmethod
    def createBid(webService, postBidJSON):
        """
        Submits a new bid to the server.
        :param webService: Instance of the WebService object used throughout the application
        :param postBidJSON: JSON object containing bid data
        :return: Bid object containing the API response
        """
        
        # Make API call and validate response
        response = webService.post(BidController.base, json=postBidJSON)
        webService.validate(response, 201, 'Failed to submit bid')

        # Return the API response
        return Bid(response.json())

    @staticmethod
    def setBidCloseDown(webService, bidID, closeDate):
        """
        Sets the close date for a bid.
        :param webService: Instance of the WebService object used throughout the application
        :param bidID: String of the ID of the bid to set the close date of
        :param closeDate: String of the close date
        :return: The API response
        """
        
        # Make API call and validate response
        response = webService.post(BidController.base + bidID + '/close-down', {'dateClosedDown': closeDate})
        webService.validate(response, 200, 'Failed to set bid close date')

        # Return the API response
        return response
    
    @staticmethod
    def deleteBid(webService, bid):
        """
        Deletes a bid from the server.
        :param webService: Instance of the WebService object used throughout the application
        :param bid: Bid object of the bid to delete
        :return: The API response
        """

        # Delete all associated messages
        for message in bid.getMessages():
            MessageController.deleteMessage(webService, message.getId())
        
        # Make API call and validate response
        response = webService.delete(BidController.base + bid.getId())
        webService.validate(response, 204, 'Failed to delete bid')

        # Return the API response
        return response