import requests

from experience.http.api_response import ApiResponse


class AuthenticationAPI:
    """
    A class to represent a Authentication API.

    Attributes
    ----------
    access_token : str
        access_token of a user
    base_url : str
        Base url of the API
    """

    def __init__(self, access_token, base_url):
        """
        Constructs all the necessary attributes for the AuthenticationAPI object

        Parameters
        ----------
        access_token : str
            access_token of a user
        base_url : str
            Base url of the API
        """
        self.access_token = access_token
        self.base_url = base_url

    def login(self, user_email, password):
        """
        Makes a POST request to the login API
        Login by using user email and password

        Parameters
        ----------
        user_email : str, mandatory
            Registered user email id
        password : str, mandatory

        Returns
        -------
        Access Token
        """
        url = self.base_url + '/v2/core/login'
        payload = {
            "user_email": user_email,
            "password": password
        }
        self.access_token = requests.post(url, data=payload)
        return self.access_token.text

    def current_user_details(self):
        """
        Makes a POST request to the current_user API
        Returns current user details using Access token

        Returns
        -------
        Current user details response
        """
        url = self.base_url + '/v2/core/current_user'
        header = {
            "Authorization": self.access_token
        }
        response = requests.post(url, headers=header)
        result = ApiResponse(response)
        return result
