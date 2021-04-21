import json
import logging
import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class UsersAPI:
    """
    A class to represent a Users API.
    Attributes
    ----------
    access_token : str
        access_token of a user
    base_url : str
        Base url of the API
    user_details : dict
        Details of the user
    """
    def __init__(self, access_token, base_url, user_details):
        """
        Constructs all the necessary attributes for the UsersAPI object
        Parameters
        ----------
        access_token : str
            access_token of a user
        base_url : str
            Base url of the API
        user_details : dict
            Details of the user
        """
        self.access_token = access_token
        self.base_url = base_url
        self.user_details = user_details
        self.response = None

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

    @staticmethod
    def request_params(params):
        user = ["email", "first_name", "last_name", "account_id"]
        user_setting_data = {"agent_sms_notify_threshold": 3.5,
                             "enable_agent_autopost": True,
                             "enable_reply_to_review": False,
                             "reply_to_review_threshold": 0,
                             "sm_max_post_per_day": 3,
                             "sm_min_duration_btw_posts": 120}
        payload = {'user': {name: params[name] for name in params if params[name] is not None and name in user}}
        payload['user'].update({"alias_email": [], "send_email": True})
        payload['user']['user_role_association'] = []
        payload['user']['user_roles'] = []
        if 'user_role' in params:
            payload['user']['user_role_association'].extend([name for name in params['user_role']])
            user_roles = [user_roles['role'] for user_roles in params['user_role']]
            for roles in user_roles:
                payload['user']['user_roles'].append(roles)
            if 'user_setting' in params:
                payload['user']['user_setting'] = {name: params[name] for name in params if params[name] is not None}
            else:
                payload['user']['user_setting'] = user_setting_data
        return payload

    def get_all_users(self, **kwargs):
        """
        Makes a GET request to the get_all_users API
        To get all the users of a given organization
        Returns
        -------
        All present users
        """
        user_details = str(self.user_details).split('ApiResponse', 1)[1]
        org_id = json.loads(user_details)
        organization_id = org_id['organization_id']
        url = f'/v2/core/organization/{organization_id}/tier_users'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_all_account_manager(self, **kwargs):
        """
        Makes a GET request to the all_account_manager API
        To get all the account manager of a given organization
        Parameters
        -------
        account_id : integer, mandatory
            ID of account
        Returns
        -------
        All account managers
        """
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}/get_account_managers'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_users(self, **kwargs):
        """
        Makes a GET request to the get_users API
        To returns a user and user settings based on the given ID.
        Parameters
        -------
        account_id : integer, mandatory
            ID of account
        Returns
        -------
        Get user success response
        """
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}/get_user'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def create_users(self, **kwargs):
        """
        Makes a POST request to the create_users API
        To create user.
        Parameters
        -------
        account_id : integer, mandatory
            ID of account
        email : string, mandatory
        first_name : string, mandatory
        last_name : string, mandatory
        Other Parameters
        -------
        user_role : dict, mandatory
        Returns
        -------
        User create response.
        """
        url = '/v2/core/users'
        logger.info("Initialising API Call")
        payload = self.request_params(kwargs)
        result = self.call_post_api(url, payload)
        return result

    def update_users(self, **kwargs):
        """
        Makes a PUT request to the update_users API
        To update a user and user settings based on the given ID
        Parameters
        -------
        user_id : integer, mandatory
            ID of the User
        Other Parameters
        -------
        tier : dict, mandatory
        Returns
        -------
        User update response.
        """
        tier = kwargs['tier']
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}'
        logger.info("Initialising API Call")
        payload = {"user": tier}
        result = self.call_update_api(url, payload)
        return result

    def deactivate_user(self, **kwargs):
        """
        Makes a PUT request to the deactivate_user API
        To deactivate a user based on the given user ID.
        Parameters
        -------
        user_id : integer, mandatory
            ID of the User
        Returns
        -------
        User is deactivated response.
        """
        user_id = kwargs['user_id']
        url = f'/v2/core/user_deactivate?user_id[]={user_id}'
        logger.info("Initialising API Call")
        result = self.call_update_api(url, kwargs)
        return result

    def get_users_settings(self, **kwargs):
        """
        Makes a GET request to the users_settings API
        To get user settings based on the given user ID.
        Parameters
        -------
        user_id : integer, mandatory
            ID of the User
        Returns
        -------
        User settings response.
        """
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}/get_user'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_users_settings(self, **kwargs):
        """
        Makes a PUT request to the users_settings API
        To update user settings based on the given user ID.
        Parameters
        -------
        user_id : integer, mandatory
            ID of the User
        Other Parameters
        -------
        user_setting : dict, mandatory
        Returns
        -------
        Updated user settings response.
        """
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}'
        logger.info("Initialising API Call")
        payload = {'user': kwargs['user_setting']}
        result = self.call_update_api(url, payload)
        return result

    def get_current_user_tiers(self, **kwargs):
        """
        Makes a GET request to the current_user_tiers API
        To get all the users under a tier.
        Parameters
        -------
        account_id : integer, mandatory
            ID of the Account
        Returns
        -------
        Users under a tier response.
        """
        account_id = kwargs['account_id']
        url = f'/v2/core/users/accounts/{account_id}/get_current_user_tiers'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result
