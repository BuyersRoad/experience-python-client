import copy
import itertools
import json
import logging
import os
import sys
import requests

from ratelimit import sleep_and_retry, limits

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from experience.http.api_response import ApiResponse
from experience.constants import base_url

logger = logging.getLogger(__name__)


class Authentication:

    def __init__(self, ):
        self.response = None

    @sleep_and_retry
    @limits(calls=100, period=60)
    def login(self, username, password):
        """Gets Access Token"""
        url = base_url + '/v2/core/login'
        payload = {
            "user_email": username,
            "password": password
        }
        self.response = requests.post(url, data=payload)
        access_token = ApiResponse(self.response)
        return access_token


class Report:
    def __init__(self, access_token):
        self.access_token = access_token
        self.response = None

    @sleep_and_retry
    @limits(calls=100, period=60)
    def call_api(self, url, param):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        payload = {name: param[name] for name in param if param[name] is not None}
        self.response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(self.response)
        return result

    @sleep_and_retry
    @limits(calls=100, period=60)
    def current_user_details(self, access_token):
        """Get User Details like account_id, organization_id"""
        url = base_url + '/v2/core/current_user'
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

    def __init__(self, access_token):
        self.access_token = access_token
        self.response = None

    @sleep_and_retry
    @limits(calls=100, period=60)
    def call_get_api(self, url, params):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        payload = {name: params[name] for name in params if params[name] is not None}
        self.response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(self.response)
        return result

    @sleep_and_retry
    @limits(calls=100, period=60)
    def call_post_api(self, url, data):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        self.response = requests.post(url, headers=header, json=data)
        result = ApiResponse(self.response)
        return result

    @sleep_and_retry
    @limits(calls=100, period=60)
    def call_update_api(self, url, data):
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        self.response = requests.put(url, headers=header, json=data)
        result = ApiResponse(self.response)
        return result

    def request_params(self, params):
        user = ["email", "first_name", "last_name", "account_id"]
        user_setting_data = {"agent_sms_notify_threshold": 3.5,
                             "enable_agent_autopost": True,
                             "enable_reply_to_review": False,
                             "reply_to_review_threshold": None,
                             "sm_max_post_per_day": 3,
                             "sm_min_duration_btw_posts": 120}
        payload = {'user': {name: params[name] for name in params if params[name] is not None and name in user}}
        payload['user'].update({"alias_email": [], "send_email": True})
        payload['user']['user_role_association'] = []
        payload['user']['user_roles'] = []
        if 'user_role' in params:
            payload['user']['user_role_association'].extend([name for name in params['user_role']])
            if filter(lambda user_role: user_role['role'] == 'Tier Manager', params['user_role']):
                payload['user']['user_roles'].append(4)
            if filter(lambda user_role: user_role['role'] == 'Agent', params['user_role']):
                payload['user']['user_roles'].append(5)
            if 'user_setting' in params:
                payload['user']['user_setting'] = {name: params[name] for name in params if params[name] is not None}
            else:
                payload['user']['user_setting'] = user_setting_data
        return payload

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

    def get_hierarchy_summary(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/accounts/{account_id}/hierarchy_summary'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def create_tiers(self, **kwargs):
        url = '/v2/core/tiers'
        logger.info("Initialising API Call")
        result = self.call_post_api(url, kwargs['tier'])
        return result

    @sleep_and_retry
    @limits(calls=100, period=60)
    def activate_tiers(self, **kwargs):
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}/activate'
        logger.info("Initialising API Call")
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        self.response = requests.put(url, headers=header, params=kwargs['id'])
        result = ApiResponse(self.response)
        return result

    def update_tiers(self, **kwargs):
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        payload = {name: kwargs[name] for name in kwargs if kwargs[name] is not None}
        result = self.call_update_api(url, payload)
        return result

    def move_tiers(self, **kwargs):
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}/move'
        logger.info("Initialising API Call")
        payload = kwargs['body']
        result = self.call_update_api(url, payload)
        return result

    def get_tiers(self, **kwargs):
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    @sleep_and_retry
    @limits(calls=100, period=60)
    def delete_tiers(self, **kwargs):
        tier_id = kwargs['tier_id']
        url = f'/v2/core/tiers/{tier_id}'
        logger.info("Initialising API Call")
        url = base_url + url
        header = {
            "Authorization": self.access_token
        }
        self.response = requests.delete(url, headers=header)
        result = ApiResponse(self.response)
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

    def create_users(self, **kwargs):
        url = '/v2/core/users'
        logger.info("Initialising API Call")
        payload = self.request_params(kwargs)
        result = self.call_post_api(url, payload)
        return result

    def update_users(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}'
        logger.info("Initialising API Call")
        payload = self.request_params(kwargs)
        result = self.call_update_api(url, payload)
        return result

    def delete_user(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/user_deactivate?user_id[]={user_id}'
        logger.info("Initialising API Call")
        result = self.call_update_api(url, kwargs)
        return result

    def get_users_settings(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}/get_user'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def update_users_settings(self, **kwargs):
        user_id = kwargs['user_id']
        url = f'/v2/core/users/{user_id}'
        logger.info("Initialising API Call")
        payload = {'user': {'user_setting': kwargs['user_setting']}}
        result = self.call_update_api(url, payload)
        return result


class Fields:

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

    @sleep_and_retry
    @limits(calls=100, period=60)
    def current_user_details(self):
        """Get User Details like account_id, organization_id"""
        url = base_url + '/v2/core/current_user'
        headers = {
            "Authorization": self.access_token
        }
        response = requests.post(url, headers=headers)
        result = ApiResponse(response)
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

    @sleep_and_retry
    @limits(calls=100, period=60)
    def get_all_account_id(self):
        """Get all the accounts from the organization"""
        url = base_url + '/v2/core/accounts'
        header = {
            "Authorization": self.access_token
        }
        logger.info("Initialising API Call")
        self.response = requests.get(url, headers=header)
        data = json.loads(self.response.text)
        account_id = []
        if data.get('data') is not None:
            for account in data.get('data'):
                result = dict(itertools.islice(account.items(), 5))
                account_id.append(result)
            result = ApiResponse(self.response)
            return result
        else:
            result = ApiResponse(self.response)
            return result

    def get_current_user_tiers(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/users/accounts/{account_id}/get_current_user_tiers'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_tier_id(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/tiers/{account_id}/hierarchy'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_tier_assignment(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/users/accounts/{account_id}/get_current_user_tiers'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_role_assignment(self, **kwargs):
        account_id = kwargs['account_id']
        url = f'/v2/core/users/accounts/{account_id}/get_current_user_tiers'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_parent_tier(self, **kwargs):
        org_id = kwargs['org_id']
        url = f'/v2/core/organization/{org_id}/hierarchy'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

    def get_tier_type(self, **kwargs):
        org_id = kwargs['org_id']
        url = f'/v2/core/organization/{org_id}/hierarchy'
        logger.info("Initialising API Call")
        result = self.call_get_api(url, kwargs)
        return result

