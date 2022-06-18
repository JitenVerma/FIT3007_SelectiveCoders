import requests
from views.ErrorPopup import ErrorPopup

class WebService:
    def __init__(self, rootURL, apiKeyPath):
        self.root_url = rootURL
        self.api_key = open(apiKeyPath, 'r').read()
        self.jwt = ''
    
    def get(self, url, params = {}):
        return requests.get(
            url = self.root_url + url,
            headers = { 'Authorization': self.api_key },
            params = params
        )
    
    def post(self, url, data = {}, params = {}, json = {}):
        return requests.post(
            url = self.root_url + url,
            headers = { 'Authorization': self.api_key },
            data = data,
            params = params,
            json = json
        )
    
    def patch(self, url, data = {}, params = {}, json = {}):
        return requests.patch(
            url = self.root_url + url,
            headers = { 'Authorization': self.api_key },
            data = data,
            params = params,
            json = json
        )
    
    def delete(self, url, data = {}, params = {}, json = {}):
        return requests.delete(
            url = self.root_url + url,
            headers = { 'Authorization': self.api_key },
            data = data,
            params = params,
            json = json
        )
    
    def setJWT(self, jwt):
        self.jwt = jwt

    def getJWT(self):
        return self.jwt
    
    def validate(self, response, expectedStatus = 200, message = 'Error', noPopup = False):
        if response.status_code != expectedStatus:
            error = response.json()['message']

            if isinstance(error, list):
                error = ", ".join(msg for msg in error)
            
            errorMessage = message + ": " + error

            if not noPopup:
                ErrorPopup(errorMessage, self)
                
            raise Exception(errorMessage)