import logging
import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class IngestTransactionAPI:

    def __init__(self, access_token, base_url):
        self.access_token = access_token
        self.base_url = base_url

    def call_post_api(self, url, data):
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        response = requests.post(url, headers=header, json=data)
        result = ApiResponse(response)
        return result

    def ingested_transaction(self, **kwargs):
        payload = kwargs['data']
        url = '/ipro/ingest_transaction'
        logger.info("Initialising API Call")
        result = self.call_post_api(url, payload)
        return result