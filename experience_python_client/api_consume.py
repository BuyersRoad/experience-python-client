import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import requests
from ratelimit import sleep_and_retry, limits

from experience_python_client.constants import base_url, login_base_url

logger = logging.getLogger(__name__)


class Login:
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


class Report:
    def __init__(self):
        self.response = None

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
