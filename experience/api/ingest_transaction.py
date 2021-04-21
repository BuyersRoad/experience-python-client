import logging
import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class IngestTransactionAPI:
    """
    A class to represent a IngestTransaction API.

    Attributes
    ----------
    access_token : str
        access_token of a user
    base_url : str
        Base url of the API
    """
    def __init__(self, access_token, base_url):
        """
        Constructs all the necessary attributes for the AuthenticationAPI object

        Parameters
        ----------
        access_token : str
            access_token of a user
        base_url : str
            Base url of the API
        """
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
        """
        Makes a POST request to the Ingest Transaction API
        Submit Transactions data to Social Survey application for surveying clients. This API supports custom data.
        You can insert those in the body as key-value pairs.

        Other Parameters
        ----------
        data : dict, mandatory
            The object that contains the servicer information

        Returns
        -------
        Response for the ingested transaction
        """
        payload = kwargs['data']
        url = '/ipro/ingest_transaction'
        logger.info("Initialising API Call")
        result = self.call_post_api(url, payload)
        return result