import requests

from experience.http.api_response import ApiResponse


class AuthenticationAPI:

    def __init__(self, access_token, base_url):
        self.access_token = access_token
        self.base_url = base_url

    def login(self, user_email, password):
        """Gets Access Token"""
        url = self.base_url + '/v2/core/login'
        payload = {
            "user_email": user_email,
            "password": password
        }
        self.access_token = requests.post(url, data=payload)
        return self.access_token.text

    def current_user_details(self):
        """Get User Details like account_id, organization_id"""
        url = self.base_url + '/v2/core/current_user'
        header = {
            "Authorization": self.access_token
        }
        response = requests.post(url, headers=header)
        result = ApiResponse(response)
        return result
