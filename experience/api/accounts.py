import json
import logging
import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class AccountsAPI:
    """
    A class to represent a Accounts API.

    Attributes
    ----------
    access_token : str
        access_token of a user
    base_url : str
        Base url of the API
    user_details : dict
        user details of the user
    """
    def __init__(self, access_token, base_url, user_details):
        """
        Constructs all the necessary attributes for the AccountsAPI object

        Parameters
        ----------
        access_token : str
            access_token of a user
        base_url : str
            Base url of the API
        user_details : dict
            user details of the user
        """
        self.access_token = access_token
        self.base_url = base_url
        self.user_details = user_details

    def call_get_api(self, url, params):
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        payload = {name: params[name] for name in params if params[name] is not None}
        response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(response)
        return result

    def call_post_api(self, url, data):
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        response = requests.post(url, headers=header, json=data)
        result = ApiResponse(response)
        return result

    def call_update_api(self, url, data):
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        response = requests.put(url, headers=header, json=data)
        result = ApiResponse(response)
        return result

    def create_account(self, **kwargs):
        """
        Makes a POST request to the create_account API
        Creates a new account in the organization.

        Other Parameters
        ----------
        vertical_id : integer, mandatory
            ID of the business category
        blueprint_id : integer, mandatory
            ID of the blueprint
        name : string, mandatory

        Returns
        -------
        account creation response
        """
        url = '/v2/core/accounts'
        logger.info("Initialising API Call")
        payload = {'account': {name: kwargs[name] for name in kwargs if kwargs[name] is not None}}
        user_details = str(self.user_details).split('ApiResponse', 1)[1]
        org_id = json.loads(user_details)
        payload['account'].update({'organization_id': org_id['organization_id']})
        result = self.call_post_api(url, payload)
        return result

    def get_account(self, **kwargs):
        """
        Makes a GET request to the get_account API
        Returns an account based on a single ID

        Parameters
        ----------
        account_id : integer, mandatory
            ID of account

        Returns
        -------
        account response
        """
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_account(self, **kwargs):
        """
        Makes a PUT request to the update_account API
        Update an account in the organization.

        Parameters
        ----------
        id : integer, mandatory
            ID of account
        Other Parameters
        ----------------
        vertical_id : integer, mandatory
            ID of the business category
        blueprint_id : integer, mandatory
            ID of the blueprint
        name : string, mandatory

        Returns
        -------
        account update response
        """
        account_id = kwargs['id']
        url = f'/v2/core/accounts/{account_id}'
        logger.info("Initialising API Call")
        payload = {'account': {name: kwargs[name] for name in kwargs if kwargs[name] is not None and
                               kwargs[name] != kwargs['id']}}
        payload['account'].update({"status": 0, "is_registration_complete": True})
        result = self.call_update_api(url, payload)
        return result

    def get_account_settings(self, **kwargs):
        """
        Makes a GET request to the account_settings API
        Returns account settings.

        Parameters
        ----------
        account_id : integer, mandatory
            ID of account

        Returns
        -------
        Account response
        """
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}/settings'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_account_settings(self, **kwargs):
        """
        Makes a PUT request to the account_settings API
        Update a account in the organization.

        Parameters
        ----------
        account_id : integer, mandatory
            ID of account

        Other Parameter
        ----------
        settings : dict, mandatory

        Returns
        -------
        account update response
        """
        account_id = kwargs['id']
        url = f'/v2/core/accounts/{account_id}/settings'
        logger.info("Initialising API Call")
        payload = {"account_settings": kwargs['account_setting']}
        result = self.call_update_api(url, payload)
        return result
