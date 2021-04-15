import logging

import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class AccountsAPI:

    def __init__(self, access_token, base_url):
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

    def create_account(self, **kwargs):
        """Creates a new account in the organization."""
        url = '/v2/core/accounts'
        logger.info("Initialising API Call")
        payload = {'account': {name: kwargs[name] for name in kwargs if kwargs[name] is not None}}
        result = self.call_post_api(url, payload)
        return result

    def get_account(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_account(self, **kwargs):
        account_id = kwargs['id']
        url = f'/v2/core/accounts/{account_id}'
        logger.info("Initialising API Call")
        payload = {'account': {name: kwargs[name] for name in kwargs if kwargs[name] is not None and
                               kwargs[name] != kwargs['id']}}
        payload['account'].update({"status": 0, "is_registration_complete": True})
        result = self.call_update_api(url, payload)
        return result

    def get_account_settings(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}/settings'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_account_settings(self, **kwargs):
        account_id = kwargs['id']
        url = f'/v2/core/accounts/{account_id}/settings'
        logger.info("Initialising API Call")
        payload = {"account_settings": kwargs['account_setting']}
        result = self.call_update_api(url, payload)
        return result
