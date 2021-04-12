import requests

from experience.constants import base_url
from experience.http.api_response import ApiResponse


class AuthenticationAPI:

    def __init__(self):
        self.access_token = None

    def login(self, user_email, password):
        """Gets Access Token"""
        url = base_url + '/v2/core/login'
        payload = {
            "user_email": user_email,
            "password": password
        }
        self.access_token = requests.post(url, data=payload)
        return self.access_token.text

    def current_user_details(self, access_token):
        """Get User Details like account_id, organization_id"""
        url = base_url + '/v2/core/current_user'
        headers = {
            "Authorization": access_token
        }
        response = requests.post(url, headers=headers)
        result = ApiResponse(response)
        return result
