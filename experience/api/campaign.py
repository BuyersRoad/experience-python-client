import logging

import requests

from experience.constants import base_url
from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class CampaignAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.response = None

    def call_api(self, url, param):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        payload = {name: param[name] for name in param if param[name] is not None}
        response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(response)
        return result

    def campaign_details(self, **kwargs):
        """Fetch the agent details for a given account and organization"""
        url = '/fetch/campaign/details'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result
