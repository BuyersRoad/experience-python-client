import itertools
import json
import logging
import os
import sys

import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from experience.http.api_response import ApiResponse
from experience.constants import base_url

logger = logging.getLogger(__name__)


class CoreAPI:

    def __init__(self, access_token):
        self.access_token = access_token
        self.response = None

    def call_get_api(self, url, params):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        payload = {name: params[name] for name in params if params[name] is not None}
        self.response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(self.response)
        return result

    def call_post_api(self, url, params):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        self.response = requests.post(url, headers=header, data=list(params.keys())[-1])
        result = ApiResponse(self.response)
        return result

    def get_business_category(self, **kwargs):
        url = "/v2/core/verticals"
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_blueprint_id(self, **kwargs):
        url = '/v2/admin/blueprints'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_organizations(self, **kwargs):
        url = '/v2/core/organizations/get_organizations'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_all_account_id(self):
        """Get all the accounts from the organization"""
        url = base_url + '/v2/core/accounts'
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
