import itertools
import json
import logging
import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class CoreAPI:
    """
    A class to represent a Core API.

    Attributes
    ----------
    access_token : str
        access_token of a user
    base_url : str
        Base url of the API
    """
    def __init__(self, access_token, base_url):
        """
        Constructs all the necessary attributes for the CoreAPI object

        Parameters
        ----------
        access_token : str
            access_token of a user
        base_url : str
            Base url of the API
        """
        self.access_token = access_token
        self.base_url = base_url
        self.response = None

    def call_get_api(self, url):
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        self.response = requests.get(url, headers=header)
        result = ApiResponse(self.response)
        return result

    def call_post_api(self, url, params):
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        self.response = requests.post(url, headers=header, data=list(params.keys())[-1])
        result = ApiResponse(self.response)
        return result

    def get_business_category(self):
        """
        Makes a GET request to the Business Category API

        Returns
        -------
        Vertical ID
        """
        url = "/v2/core/verticals"
        logger.info("Initialising API Call")
        result = self.call_get_api(url)
        return result

    def get_blueprint_id(self):
        """
        Makes a GET request to the Blueprint API

        Returns
        -------
        Blueprint ID
        """
        url = '/v2/admin/blueprints'
        logger.info("Initialising API Call")
        result = self.call_get_api(url)
        return result

    def get_all_account_id_and_name(self):
        """
        Makes a GET request to the Account ID and Name API
        Gets all the accounts from the organization

        Returns
        -------
        All account id with name
        """
        url = self.base_url + '/v2/core/accounts'
        header = {
            "Authorization": self.access_token
        }
        logger.info("Initialising API Call")
        response = requests.get(url, headers=header)
        data = json.loads(response.text)
        account_id = []
        if data.get('data') is not None:
            for account in data.get('data'):
                result = dict(itertools.islice(account.items(), 5))
                account_id.append(result)
            result = ApiResponse(response)
            return result
        else:
            result = ApiResponse(response)
            return result
