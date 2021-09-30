import logging

import requests

from experience.http.api_response import ApiResponse

logger = logging.getLogger(__name__)


class ReportsAPI:

    def __init__(self, access_token, base_url):
        self.access_token = access_token
        self.base_url = base_url
        self.response = None

    def call_api(self, url, param):
        url = self.base_url + url
        header = {
            "Authorization": self.access_token
        }
        payload = {name: param[name] for name in param if param[name] is not None}
        self.response = requests.get(url, headers=header, params=payload)
        result = ApiResponse(self.response)
        return result

    def activity_feed(self, **kwargs):
        """ Gets the history of activities performed by different users in a single account"""
        url = "/fetch/activityfeed"
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
        url = "/generate/reviews/management/report"
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
        url = '/generate/tier/ranking/report'
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
        #  TODO - check where this needs to be placed

        """ Fetch the agent details for a given account and organization"""
        url = '/fetch/agent/details'
        logger.info("Initialising API Call")
        result = self.call_api(url, kwargs)
        return result
