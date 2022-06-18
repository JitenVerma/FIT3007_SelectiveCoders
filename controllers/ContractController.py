from models.Contract import Contract
from datetime import datetime

class ContractController():
    """
    ContractController class provides methods relating to the /contract routes in the API.
    All methods are static so an object does not need to be instantiated.
    """
    base = 'contract/'     # Static variable of the base API route for user API calls

    @staticmethod
    def getContracts(webService):
        """
        Get all contracts currently in the system as an array of contract objects.
        :param webService: Instance of the WebService object used throughout the application
        :return: Array of Contract objects containing the API response
        """
        
        # Make API call and validate response
        response = webService.get(ContractController.base)
        webService.validate(response, 200, 'Failed to get contracts')

        # Instantiate Contract objects from response
        responseJSON = response.json()
        contracts = []

        for contract in responseJSON:
            contracts.append(Contract(contract))

        # Return the API response
        return contracts

    @staticmethod
    def getContract(webService, contractID):
        """
        Get a contract by it's ID
        :param webService: Instance of the WebService object used throughout the application
        :param contractID: String ID of the contract to get
        :return: Contract object containing the API response
        """
        
        # Make API call and validate response
        response = webService.get(ContractController.base + contractID)
        webService.validate(response, 200, 'Failed to get contract')

        # Return the API response
        return Contract(response.json())
    
    @staticmethod
    def addContract(webService, contractJSON):
        """
        Submits a new contract to the server to be added.
        :param webService: Instance of the WebService object used throughout the application
        :param contractJSON: JSON object containing contract data
        :return: Contract object containing the API response
        """
        
        # Make API call and validate response
        response = webService.post(ContractController.base, json=contractJSON)
        webService.validate(response, 201, 'Failed to add contract')

        # Return the API response
        return Contract(response.json())

    @staticmethod
    def signContract(webService, contractID, dateSigned):
        """
        Signs a contract.
        :param webService: Instance of the WebService object used throughout the application
        :param contractID: String ID of the contract to sign
        :param dateSigned: String date that the contract is signed
        :return: The API response
        """
        
        # Make API call and validate response
        response = webService.post(ContractController.base + contractID + '/sign', data={'dateSigned': dateSigned})
        webService.validate(response, 200, 'Failed to sign contract')

        # Return the API response
        return response
    
    @staticmethod
    def updateContract(webService, contractID, data):
        """
        Partially update a contract (patch) with the provided data
        :param webService: Instance of the WebService object used throughout the application
        :param contractID: string of the contractID of the contract to update
        :param data: JSON object of updated contract data
        :return: The API response data
        """

        # Make API call and validate response
        response = webService.patch(ContractController.base + contractID, json=data)
        webService.validate(response, 200, 'Failed to update contract information')

        # Return the API response
        return response.json()

    @staticmethod
    def setFirstPartySigned(webService, contract):
        """
        Sets the 'first party signed' field to True for a given contract
        :param webService: Instance of the WebService object used throughout the application
        :param contract: Contract of the contract to update
        :param data: JSON object of updated contract data
        :return: Contract object with the API response data
        """

        # Set firstPartySigned to True
        contract = ContractController.getContract(webService, contract.getId())
        data = { 'additionalInfo': contract.getAdditionalInfo().toJSONObject() }
        data['additionalInfo']['firstPartySigned'] = True

        # Update the contract on the server
        response = ContractController.updateContract(webService, contract.getId(), data)
        newContract = Contract(response)

        # Check if contract is now signed by both parties, and set the date signed
        if newContract.getAdditionalInfo().isFirstPartySigned():
            if newContract.getAdditionalInfo().isSecondPartySigned():
                if newContract.getDateSigned() == None:
                    dateSigned = (datetime.now()).isoformat()
                    ContractController.signContract(webService, newContract.getId(), dateSigned)
                    newContract.setDateSigned(dateSigned)

        # Return the API response
        return newContract

    @staticmethod
    def setSecondPartySigned(webService, contract):
        """
        Sets the 'second party signed' field to True for a given contract
        :param webService: Instance of the WebService object used throughout the application
        :param contract: Contract of the contract to update
        :param data: JSON object of updated contract data
        :return: Contract object with the API response data
        """

        # Set secondPartySigned to True
        contract = ContractController.getContract(webService, contract.getId())
        data = { 'additionalInfo': contract.getAdditionalInfo().toJSONObject() }
        data['additionalInfo']['secondPartySigned'] = True

        # Update the contract on the server
        response = ContractController.updateContract(webService, contract.getId(), data)
        newContract = Contract(response)

        # Check if contract is now signed by both parties, and set the date signed
        if newContract.getAdditionalInfo().isFirstPartySigned():
            if newContract.getAdditionalInfo().isSecondPartySigned():
                if newContract.getDateSigned() == None:
                    dateSigned = (datetime.now()).isoformat()
                    ContractController.signContract(webService, newContract.getId(), dateSigned)
                    newContract.setDateSigned(dateSigned)

        # Return the API response
        return newContract
    
    @staticmethod
    def deleteContract(webService, contractID):
        """
        Deletes a contract from the server
        :param webService: Instance of the WebService object used throughout the application
        :param contractID: String ID of the contract to delete
        :return: The API response
        """
        
        # Make API call and validate response
        response = webService.delete(ContractController.base + contractID)
        webService.validate(response, 204, 'Failed to delete contract')

        # Return the API response
        return response