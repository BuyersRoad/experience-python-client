import logging

import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class HierarchyAPI:

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

    def get_hierarchy_summary(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}/hierarchy_summary'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def list_hierarchy(self, **kwargs):
        org_id = kwargs['org_id']
        url = f'/v2/core/organization/{org_id}/hierarchy'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result
