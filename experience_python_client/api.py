import logging
import os
import sys

from experience_python_client.http.api_response import ApiResponse

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import requests
from ratelimit import sleep_and_retry, limits

from experience_python_client.constants import base_url, login_base_url

logger = logging.getLogger(__name__)


class Authentication:

    def __init__(self):
        self.response = None

    @sleep_and_retry
    @limits(calls=100, period=60)
    def login(self, username, password):
        """Gets Access Token"""
        url = login_base_url + '/v2/core/login'
        payload = {
            "user_email": username,
            "password": password
        }
        login_response = requests.post(url, data=payload)
        access_token = ApiResponse(login_response)
        return access_token


class Report:
    def __init__(self):
        self.response = None

    @sleep_and_retry
    @limits(calls=100, period=60)
    def call_api(self, url, param):
        url = base_url + url
        header = {
            "Authorization": param['access_token']
        }
        payload = {name: param[name] for name in param if param[name] is not None}
        self.response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(self.response)
        return result

    @sleep_and_retry
    @limits(calls=100, period=60)
    def current_user_details(self, access_token):
        """Get User Details like account_id, organization_id"""
        url = login_base_url + '/v2/core/current_user'
        print(url)
        headers = {
            "Authorization": access_token
        }
        response = requests.post(url, headers=headers)
        result = ApiResponse(response)
        return result

    def activity_feed(self, **kwargs):
        """ Gets the history of activities performed by different users in a single account"""
        url = "/fetch/activityfeed"
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def tier_details(self, **kwargs):
        """Fetch the tier hierarchy for a given account and organization"""
        url = "/fetch/tier/details"
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def agent_ranking_report(self, **kwargs):
        """Generates the agent ranking report for a given campaign for a given month/year"""
        url = "/generate/agent/ranking/report"
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def hierarchy_details_report(self, **kwargs):
        """Generates the hierarchy user details and hierarchy tier details report for a given account"""
        url = "/generate/hierarchy/details/report"
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def incomplete_survey_report(self, **kwargs):
        """Generates the incomplete surveys report for a given campaign"""
        url = "/generate/incomplete/surveys/report"
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def nps_report(self, **kwargs):
        """Generate the nps report for a given account"""
        url = "/generate/nps/report"
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def publish_history_report(self, **kwargs):
        """Generates the publish history report for a given account/tier for the current point of time"""
        url = "/generate/publish/history/report"
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def reviews_management_report(self, **kwargs):
        """Generates the reviews management  report for a given account/tier for a given date range"""
        url = "/generate/publish/history/report"
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def survey_results_report(self, **kwargs):
        """Generates the survey results report for a given campaign"""
        url = '/generate/survey/results/report'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def survey_statistics_report(self, **kwargs):
        """ Generates the survey statistics report for a given account for a given range period"""
        url = '/generate/survey/statistics/report'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def ranking_report_tier(self, **kwargs):
        """Generates the survey statistics report for a given account for a given range period"""
        url = 'generate/tier/ranking/report'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def user_details_report(self, **kwargs):
        """Generates the user details report for a given account"""
        url = '/generate/user/details/report'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def verified_users_report(self, **kwargs):
        """Generates the verified users report for a given account/tier for the current point of time"""
        url = '/generate/verified/users/report'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def agent_details(self, **kwargs):
        """ Fetch the agent details for a given account and organization"""
        url = '/fetch/agent/details'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result

    def campaign_details(self, **kwargs):
        """Fetch the agent details for a given account and organization"""
        url = '/fetch/campaign/details'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result


class Hierarchy:

    def __init__(self):
        self.response = None

    def call_get_api(self, url, params):
        url = login_base_url + url
        header = {
            "Authorization": params['access_token']
        }
        payload = {name: params[name] for name in params if params[name] is not None}
        self.response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(self.response)
        return result

    def call_post_api(self, url, params):
        url = login_base_url + url
        header = {
            "Authorization": params['access_token']
        }
        self.response = requests.post(url, headers=header, data=list(params.keys())[-1])
        result = ApiResponse(self.response)
        return result

    def call_update_api(self, url, params):
        url = login_base_url + url
        header = {
            "Authorization": params['access_token']
        }
        self.response = requests.put(url, headers=header, params=params['id'], data=list(params.keys())[-1])
        result = ApiResponse(self.response)
        return result

    def create_account(self, **kwargs):
        """Creates a new account in the organization."""
        url = '/v2/core/accounts'
        logger.info("Initialising API Call")
        result = self.call_post_api(url, kwargs)
        return result

    def get_account(self, **kwargs):
        url = '/v2/core/accounts'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_account(self, **kwargs):
        url = '/v2/core/accounts'
        logger.info("Initialising API Call")
        result = self.call_update_api(url, kwargs)
        return result

    def get_account_settings(self, **kwargs):
        account_id = kwargs['id']
        url = f'/v2/core/accounts/{account_id}/settings'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_account_settings(self, **kwargs):
        account_id = kwargs['id']
        url = f'/v2/core/accounts/{account_id}/settings'
        logger.info("Initialising API Call")
        result = self.call_update_api(url, kwargs)
        return result

    def get_hierarchy_summary(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}/hierarchy_summary'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def create_tiers(self, **kwargs):
        url = '/v2/core/tiers'
        logger.info("Initialising API Call")
        result = self.call_post_api(url, kwargs)
        return result

    def activate_tiers(self, **kwargs):
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}/activate'
        logger.info("Initialising API Call")
        url = login_base_url + url
        header = {
            "Authorization": kwargs['access_token']
        }
        self.response = requests.put(url, headers=header, params=kwargs['id'])
        result = ApiResponse(self.response)
        return result

    def update_tiers(self, **kwargs):
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        result = self.call_update_api(url, kwargs)
        return result

    def move_tiers(self, **kwargs):
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}/move'
        logger.info("Initialising API Call")
        result = self.call_update_api(url, kwargs)
        return result

    def get_tiers(self, **kwargs):
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def delete_tiers(self, **kwargs):
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        url = login_base_url + url
        header = {
            "Authorization": kwargs['access_token']
        }
        payload = {name: kwargs[name] for name in kwargs if kwargs[name] is not None}
        self.response = requests.delete(url, headers=header, params=payload)
        result = ApiResponse(self.response)
        return result

    def get_tier_settings(self, **kwargs):
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}/settings'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_tier_settings(self, **kwargs):
        tier_id = kwargs['id']
        url = f'/v2/core/tiers/{tier_id}/settings'
        logger.info("Initialising API Call")
        result = self.call_update_api(url, kwargs)
        return result

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
