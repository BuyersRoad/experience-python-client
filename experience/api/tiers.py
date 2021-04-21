import logging
import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class TiersAPI:
    """
    A class to represent a Tiers API.
    Attributes
    ----------
    access_token : str
        access_token of a user
    base_url : str
        Base url of the API
    """
    def __init__(self, access_token, base_url):
        """
        Constructs all the necessary attributes for the TiersAPI object
        Parameters
        ----------
        access_token : str
            access_token of a user
        base_url : str
            Base url of the API
        """

        self.access_token = access_token
        self.base_url = base_url

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

    def create_tier(self, **kwargs):
        """
        Makes a POST request to the create_tier API
        To create a new tier.
        Other Parameters
        ----------
        account_id : integer, mandatory
            ID of the account
        tier_category_id : integer, mandatory
            ID of the tier category
        parent : integer, mandatory
        name : string, mandatory
        label : string, mandatory
        description : string, mandatory
        Returns
        -------
        Tier creation response
        """
        url = '/v2/core/tiers'
        logger.info("Initialising API Call")
        result = self.call_post_api(url, kwargs['tier'])
        return result

    def activate_tier(self, **kwargs):
        """
        Makes a PUT request to the activate_tier API
        To activate given tier and its associates
        Parameters
        ----------
        tier_id : integer, mandatory
            ID of the tier
        Returns
        -------
        Tier activate response
        """
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}/activate'
        logger.info("Initialising API Call")
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        response = requests.put(url, headers=header)
        result = ApiResponse(response)
        return result

    def update_tier(self, **kwargs):
        """
        Makes a PUT request to the update_tier API
        To update a tier based on the given ID.
        Parameters
        ----------
        tier_id : integer, mandatory
           ID of the tier
        Other Parameters
        ----------
        name : string, mandatory
        label : string, mandatory
        description : string, mandatory
        Returns
        -------
        Tier update response
        """
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        payload = {name: kwargs[name] for name in kwargs if kwargs[name] is not None}
        result = self.call_update_api(url, payload)
        return result

    def move_tier(self, **kwargs):
        """
        Makes a PUT request to the move_tier API
        To move tier from one parent to other.
        Parameters
        ----------
        tier_id : integer, mandatory
           ID of the tier
        Other Parameters
        ----------
        destination_parent_tier_id : integer, mandatory
        destination_order : integer, mandatory
        Returns
        -------
        Tier move response
        """
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}/move'
        logger.info("Initialising API Call")
        payload = kwargs['body']
        result = self.call_update_api(url, payload)
        return result

    def get_tier(self, **kwargs):
        """
        Makes a GET request to the get_tier API
        To returns a tier based on the given ID.
        Parameters
        ----------
        tier_id : integer, mandatory
           ID of the tier
        Returns
        -------
        Tier success response
        """
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def delete_tier(self, **kwargs):
        """
        Makes a DELETE request to the delete_tier API
        To destroy a tier based on the given ID
        Parameters
        ----------
        tier_id : integer, mandatory
            ID of the tier
        Returns
        -------
        Tier delete response
        """
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        response = requests.delete(url, headers=header)
        result = ApiResponse(response)
        return result

    def get_tier_settings(self, **kwargs):
        """
        Makes a GET request to the get_tier_settings API
        Get the settings of a particular tier
        Parameters
        ----------
        tier_id : integer, mandatory
           ID of the tier
        Returns
        -------
        Tier settings response
        """
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}/settings'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_tier_settings(self, **kwargs):
        """
        Makes a PUT request to the update_tier_settings API
        Update the settings of a particular tier
        Parameters
        ----------
        tier_id : integer, mandatory
           ID of the tier
        Other Parameters
        ----------
        tier_setting : dict, mandatory
        Returns
        -------
        Tier settings response
        """
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}/settings'
        logger.info("Initialising API Call")
        payload = {"tier_settings": kwargs['tier_setting']}
        result = self.call_update_api(url, payload)
        return result

    def get_hierarchy_by_account(self, **kwargs):
        """
        Makes a GET request to the hierarchy_by_account API
        To get hierarchy from account_id.
        Parameters
        ----------
        account_id : integer, mandatory
           ID of the account
        Returns
        -------
        Hierarchy by account response
        """
        account_id = kwargs['account_id']
        url = f'/v2/core/tiers/{account_id}/hierarchy'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def call_api(self, url, param):
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        payload = {name: param[name] for name in param if param[name] is not None}
        response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(response)
        return result
