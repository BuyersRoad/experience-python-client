import logging

import requests

from experience.constants import base_url
from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class UsersAPI:

    def __init__(self, access_token):
        self.access_token = access_token

    def call_get_api(self, url, params):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        payload = {name: params[name] for name in params if params[name] is not None}
        response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(response)
        return result

    def call_post_api(self, url, data):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        response = requests.post(url, headers=header, json=data)
        result = ApiResponse(response)
        return result

    def call_update_api(self, url, data):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        response = requests.put(url, headers=header, json=data)
        result = ApiResponse(response)
        return result

    def request_params(self, params):
        user = ["email", "first_name", "last_name", "account_id"]
        user_setting_data = {"agent_sms_notify_threshold": 3.5,
                             "enable_agent_autopost": True,
                             "enable_reply_to_review": False,
                             "reply_to_review_threshold": None,
                             "sm_max_post_per_day": 3,
                             "sm_min_duration_btw_posts": 120}
        payload = {'user': {name: params[name] for name in params if params[name] is not None and name in user}}
        payload['user'].update({"alias_email": [], "send_email": True})
        payload['user']['user_role_association'] = []
        payload['user']['user_roles'] = []
        if 'user_role' in params:
            payload['user']['user_role_association'].extend([name for name in params['user_role']])
            if filter(lambda user_role: user_role['role'] == 'Tier Manager', params['user_role']):
                payload['user']['user_roles'].append(4)
            if filter(lambda user_role: user_role['role'] == 'Agent', params['user_role']):
                payload['user']['user_roles'].append(5)
            if 'user_setting' in params:
                payload['user']['user_setting'] = {name: params[name] for name in params if params[name] is not None}
            else:
                payload['user']['user_setting'] = user_setting_data
        return payload

    def get_all_users(self, **kwargs):
        org_id = kwargs['org_id']
        url = f'/v2/core/organization/{org_id}/tier_users'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_all_account_manager(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}/get_account_managers'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_users(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}/get_user'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def create_users(self, **kwargs):
        url = '/v2/core/users'
        logger.info("Initialising API Call")
        payload = self.request_params(kwargs)
        result = self.call_post_api(url, payload)
        return result

    def update_users(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}'
        logger.info("Initialising API Call")
        payload = {"user":{kwargs['tier']}}
        result = self.call_update_api(url, payload)
        return result

    def deactivate_user(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/user_deactivate?user_id[]={user_id}'
        logger.info("Initialising API Call")
        result = self.call_update_api(url, kwargs)
        return result

    def get_users_settings(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}/get_user'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_users_settings(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}'
        logger.info("Initialising API Call")
        payload = {'user': kwargs['user_setting']}
        result = self.call_update_api(url, payload)
        return result

    def get_current_user_tiers(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/users/accounts/{account_id}/get_current_user_tiers'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result