import logging
import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class TiersAPI:

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

    def create_tier(self, **kwargs):
        url = '/v2/core/tiers'
        logger.info("Initialising API Call")
        result = self.call_post_api(url, kwargs['tier'])
        return result

    def activate_tier(self, **kwargs):
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
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        payload = {name: kwargs[name] for name in kwargs if kwargs[name] is not None}
        result = self.call_update_api(url, payload)
        return result

    def move_tier(self, **kwargs):
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}/move'
        logger.info("Initialising API Call")
        payload = kwargs['body']
        result = self.call_update_api(url, payload)
        return result

    def get_tier(self, **kwargs):
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def delete_tier(self, **kwargs):
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
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}/settings'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_tier_settings(self, **kwargs):
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}/settings'
        logger.info("Initialising API Call")
        payload = {"tier_settings": kwargs['tier_setting']}
        result = self.call_update_api(url, payload)
        return result

    def get_hierarchy_by_account(self, **kwargs):
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



