import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import requests
from ratelimit import sleep_and_retry, limits

from experience_python_client.constants import base_url, login_base_url

logger = logging.getLogger(__name__)


class Client:
    def __init__(self):
        self.response = None

    @sleep_and_retry
    @limits(calls=100, period=60)
    def login(self, username, password):
        """Gets Access Token"""
        try:
            url = login_base_url + '/v2/core/login'
            payload = {
                "user_email": username,
                "password": password
            }
            login_response = requests.post(url, data=payload)
            if self.response.status_code == 200:
                logger.info("Logged in Successfully")
                return login_response.json()
            else:
                logger.error("Exception raised while Consuming Login API", self.response.status_code)
        except Exception as err:
            logger.error("Exception raised due to" + str(err))

    @sleep_and_retry
    @limits(calls=100, period=60)
    def call_api(self, url, param):
        try:
            url = base_url + url
            header = {
                "Authorization": param['access_token']
            }
            payload = {name: param[name] for name in param if param[name] is not None}
            self.response = requests.get(url, headers=header, params=payload)
            if self.response.status_code == 200:
                logger.info("API -" + url + "Consumed Successfully")
                return self.response
            else:
                logger.error("Exception raised while Consuming API")
        except Exception as err:
            logger.error("Exception raised due to" + str(err))

    @sleep_and_retry
    @limits(calls=100, period=60)
    def current_user_details(self, access_token):
        """Get User Details like account_id, organization_id"""
        try:
            url = login_base_url + '/v2/core/current_user'
            print(url)
            headers = {
                "Authorization": access_token
            }
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                logger.info("Got User Details Successfully")
                return response.json()
            else:
                logger.error("Exception raised while Consuming User API", response.status_code)
        except Exception as err:
            logger.error("Exception raised due to" + str(err))

    def activity_feed(self, **kwargs):
        """ Gets the history of activities performed by different users in a single account"""
        url = "/fetch/activityfeed"
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def tier_details(self, **kwargs):
        """Fetch the tier hierarchy for a given account and organization"""
        url = "/fetch/tier/details"
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def agent_ranking_report(self, **kwargs):
        """Generates the agent ranking report for a given campaign for a given month/year"""
        url = "/generate/agent/ranking/report"
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def hierarchy_details_report(self, **kwargs):
        """Generates the hierarchy user details and hierarchy tier details report for a given account"""
        url = "/generate/hierarchy/details/report"
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def incomplete_survey_report(self, **kwargs):
        """Generates the incomplete surveys report for a given campaign"""
        url = "/generate/incomplete/surveys/report"
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def nps_report(self, **kwargs):
        """Generate the nps report for a given account"""
        url = "/generate/nps/report"
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def publish_history_report(self, **kwargs):
        """Generates the publish history report for a given account/tier for the current point of time"""
        url = "/generate/publish/history/report"
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def reviews_management_report(self, **kwargs):
        """Generates the reviews management  report for a given account/tier for a given date range"""
        url = "/generate/publish/history/report"
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def survey_results_report(self, **kwargs):
        """Generates the survey results report for a given campaign"""
        url = '/generate/survey/results/report'
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def survey_statistics_report(self, **kwargs):
        """ Generates the survey statistics report for a given account for a given range period"""
        url = '/generate/survey/statistics/report'
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def ranking_report_tier(self, **kwargs):
        """Generates the survey statistics report for a given account for a given range period"""
        url = 'generate/tier/ranking/report'
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def user_details_report(self, **kwargs):
        """Generates the user details report for a given account"""
        url = '/generate/user/details/report'
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def verified_users_report(self, **kwargs):
        """Generates the verified users report for a given account/tier for the current point of time"""
        url = '/generate/verified/users/report'
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def agent_details(self, **kwargs):
        """ Fetch the agent details for a given account and organization"""
        url = '/fetch/agent/details'
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()

    def campaign_details(self, **kwargs):
        """Fetch the agent details for a given account and organization"""
        url = '/fetch/campaign/details'
        logger.info("Initialising API Call")
        self.call_api(url, kwargs)
        return self.response.json()


class Hierarchy:

    def __init__(self):
        self.response = None

    def call_get_api(self, url, params):
        try:
            url = login_base_url + url
            header = {
                "Authorization": params['access_token']
            }
            payload = {name: params[name] for name in params if params[name] is not None}
            self.response = requests.get(url, headers=header, params=payload)
            print(url, payload)
            if self.response.status_code == 200:
                logger.info("API -" + url + "Consumed Successfully")
                return self.response
            else:
                logger.error(str(self.response.json()))
        except Exception as err:
            logger.error("Exception raised due to" + str(err))

    def call_post_api(self, url, params):
        try:
            url = login_base_url + url
            header = {
                "Authorization": params['access_token']
            }
            self.response = requests.post(url, headers=header, data=list(params.keys())[-1])
            if self.response.status_code == 200:
                logger.info("API consumed Successfully")
                return self.response.json()
            else:
                logger.error(str(self.response.json()))
        except Exception as err:
            logger.error("Exception raised due to" + str(err))

    def call_update_api(self, url, params):
        try:
            url = login_base_url + url
            header = {
                "Authorization": params['access_token']
            }
            self.response = requests.put(url, headers=header, params=params['id'], data=list(params.keys())[-1])
            if self.response.status_code == 200:
                logger.info("API -" + url + "Consumed Successfully")
                return self.response.json()
            else:
                logger.error(str(self.response.json()))
        except Exception as err:
            logger.error("Exception raised due to" + str(err))

    def create_account(self, **kwargs):
        """Creates a new account in the organization."""
        url = '/v2/core/accounts'
        logger.info("Initialising API Call")
        self.call_post_api(url, kwargs)
        return self.response

    def get_account(self, **kwargs):
        url = '/v2/core/accounts'
        logger.info("Initialising API Call")
        self.call_get_api(url, kwargs)
        return self.response.json()

    def update_account(self, **kwargs):
        url = '/v2/core/accounts'
        logger.info("Initialising API Call")
        self.call_update_api(url, kwargs)
        return self.response

    def get_account_settings(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/accounts/{id}/settings'
        logger.info("Initialising API Call")
        self.call_get_api(url, kwargs)
        return self.response.json()

    def update_account_settings(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/accounts/{id}/settings'
        logger.info("Initialising API Call")
        self.call_update_api(url, kwargs)
        return self.response.json()

    def get_hierarchy_summary(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}/hierarchy_summary'
        logger.info("Initialising API Call")
        self.call_get_api(url, kwargs)
        return self.response.json()

    def create_tiers(self, **kwargs):
        url = '/v2/core/tiers'
        logger.info("Initialising API Call")
        self.call_post_api(url, kwargs)
        return self.response.json()

    def activate_tiers(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/tiers/{id}/activate'
        logger.info("Initialising API Call")
        try:
            url = login_base_url + url
            header = {
                "Authorization": kwargs['access_token']
            }
            self.response = requests.put(url, headers=header, params=kwargs['id'])
            if self.response.status_code == 200:
                logger.info("API -" + url + "Consumed Successfully")
                return self.response.json()
            else:
                logger.error(str(self.response.json()))
        except Exception as err:
            logger.error("Exception raised due to" + str(err))

    def update_tiers(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/tiers/{id}'
        logger.info("Initialising API Call")
        self.call_update_api(url, kwargs)
        return self.response.json()

    def move_tiers(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/tiers/{id}/move'
        logger.info("Initialising API Call")
        self.call_update_api(url, kwargs)
        return self.response.json()

    def get_tiers(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/tiers/{id}'
        logger.info("Initialising API Call")
        self.call_get_api(url, kwargs)
        return self.response.json()

    def delete_tiers(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/tiers/{id}'
        logger.info("Initialising API Call")
        try:
            url = login_base_url + url
            header = {
                "Authorization": kwargs['access_token']
            }
            payload = {name: kwargs[name] for name in kwargs if kwargs[name] is not None}
            self.response = requests.delete(url, headers=header, params=payload)
            print(url, payload)
            if self.response.status_code == 200:
                logger.info("API -" + url + "Consumed Successfully")
                return self.response.json()
            else:
                logger.error(str(self.response.json()))
                return self.response.json()
        except Exception as err:
            logger.error("Exception raised due to" + str(err))

    def get_tier_settings(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/tiers/{id}/settings'
        logger.info("Initialising API Call")
        self.call_get_api(url, kwargs)
        return self.response.json()

    def update_tier_settings(self, **kwargs):
        id = kwargs['id']
        url = f'/v2/core/tiers/{id}/settings'
        logger.info("Initialising API Call")
        self.call_update_api(url, kwargs)
        return self.response.json()