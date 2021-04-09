import requests

from experience.constants import base_url
from experience.http.api_response import ApiResponse


class AuthenticationAPI:

    def __init__(self, ):
        self.response = None

    def login(self, username, password):
        """Gets Access Token"""
        url = base_url + '/v2/core/login'
        payload = {
            "user_email": username,
            "password": password
        }
        self.response = requests.post(url, data=payload)
        access_token = ApiResponse(self.response)
        return access_token

    def current_user_details(self, access_token):
        """Get User Details like account_id, organization_id"""
        url = base_url + '/v2/core/current_user'
        headers = {
            "Authorization": access_token
        }
        response = requests.post(url, headers=headers)
        result = ApiResponse(response)
        return result
