import sys
from controllers.WebService import WebService
from views.Login import Login

class App:
    def __init__(self):
        sys.path.append("/")
        self.webService = WebService('https://fit3077.com/api/v2/', 'api_key.txt')
        Login(self.webService)

# Main code
def main():
    App()

if __name__ == "__main__":
    main()