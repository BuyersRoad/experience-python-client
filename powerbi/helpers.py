import os
import sqlite3

from experience.api.reports import ReportsAPI
import json
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import config


class PowerBI_Reports(ReportsAPI):

    def __init__(self, access_token, base_url):
        super().__init__(access_token, base_url)

    def survey_email_report(self, **kwargs):
        """to generate the survey email delivery report"""
        url = "/generate/survey/email/delivery/status/report"
        result = self.call_api(url, kwargs)
        return result

    def sms_delivery_report(self, **kwargs):
        url = "/generate/sms/delivery/statistics/report"
        result = self.call_api(url, kwargs)
        return result

    def digest_report(self, **kwargs):
        url = "/generate/digest/report"
        result = self.call_api(url, kwargs)
        return result

    def nps_trend_report(self, **kwargs):
        url = "/generate/nps/trend/report"
        result = self.call_api(url, kwargs)
        return result

    def account_statistics_report(self, **kwargs):
        url = "/generate/account/statistics/report"
        result = self.call_api(url, kwargs)
        return result

    def mismatch_report(self, account_id, **kwargs):
        url = f"/v2/ipro/accounts/{account_id}/mismatches"
        result = self.call_api(url, kwargs)
        return result

    def user_ranking_report(self, account_id, **kwargs):
        url = f"/v2/core/accounts/{account_id}/leaderboard"
        result = self.call_api(url, kwargs)
        return result

    def company_user_report(self, org_id, **kwargs):
        url = f"/v2/core/organization/{org_id}/tier_users"
        result = self.call_api(url, kwargs)
        return result


def get_date_range(date):
    today_date = dt.now()
    end_date = dt.now().strftime("%Y-%m-%d")
    start_date = (today_date - timedelta(days=int(date))).strftime("%Y-%m-%d")
    return [start_date, end_date]


def get_report_data(report, v, k, account_id, account_name, logger, base_dir, campaign_data=None):
    logger.info(f"Generating report for {k}")
    account_dir = f'{base_dir}/{account_name}'
    if not os.path.exists(account_dir):
        os.mkdir(account_dir)
    path = f"{account_dir}/{k}"
    if not (os.path.exists(path)):
        os.mkdir(path)
    date_range = get_date_range(config.data_range)
    cur_date_time = ("{:%Y_%m_%d}".format(dt.now()))
    try:
        if v == "surveyresults":
            data = report.survey_results_report(account_id=f"{account_id}", report_format='json',
                                                range_period=json.dumps(date_range))
            data_json = json.loads(data.text)
            result = data_json.get("survey_results")
            filename = f"{path}/{v}_{cur_date_time}.csv"
            return result, filename
        elif v == "reviewsmanagement":
            data = report.reviews_management_report(account_id=f"{account_id}", report_format='json',
                                                    range_period=json.dumps(date_range))
            data_json = json.loads(data.text)
            result = data_json.get("reviews_management_tier_details")
            filename = f"{path}/{v}_{cur_date_time}.csv"
            return result, filename
        elif v == "surveystatistics":
            data = report.survey_statistics_report(account_id=f"{account_id}", report_format='json',
                                                   range_period=json.dumps(date_range))
            data_json = json.loads(data.text)
            filename = f"{path}/{v}_{cur_date_time}.csv"
            return data_json, filename
        elif v == "publishhistory":
            data = report.publish_history_report(report_name="Publish History",
                                                 account_id=f"{account_id}",
                                                 account_name=f"{account_name}",
                                                 action="Download", report_format="json",
                                                 tier_data=[
                                                     {"label": "All Tier", "value": f"{account_id}"}])
            data_json = json.loads(data.text)
            result = data_json.get("agent_details")
            filename = f"{path}/{v}_all_time.csv"
            return result, filename
        elif v == "hierarchydetails":
            data = report.hierarchy_details_report(report_name="Hierarchy Details",
                                                   account_id=f"{account_id}",
                                                   account_name=f"{account_name}",
                                                   action="Download", report_format="json", period=config.month)
            data_json = json.loads(data.text)
            result = data_json.get("hierarchy_user_details")
            filename = f"{path}/{v}_{config.month}.csv"
            return result, filename
        elif v == "verifiedusers":
            data = report.verified_users_report(report_name="Verified Users",
                                                account_id=f"{account_id}",
                                                account_name=f"{account_name}",
                                                action="Download", report_format="json",
                                                tier_data=[{"label": "All Tier", "value": f"{account_id}"}])
            data_json = json.loads(data.text)
            result = data_json.get("verified_user_details")
            filename = f"{path}/{v}_all_time.csv"
            return result, filename
        elif v == "npstrend":
            data = report.nps_trend_report(report_name="NPS Trend Report",
                                           account_id=f"{account_id}",
                                           account_name=f"{account_name}",
                                           action="Download", report_format="json", period=config.month)
            data_json = json.loads(data.text)
            result = data_json.get("loading test-Tier")
            filename = f"{path}/{v}_{config.month}.csv"
            return result, filename
        elif v == "accountstatistics":
            data = report.account_statistics_report(report_name="Account Statistics Report",
                                                    account_id=f"{account_id}",
                                                    account_name=f"{account_name}",
                                                    action="Download", report_format="json")
            data_json = json.loads(data.text)
            result = data_json.get("accounts")
            filename = f"{path}/{v}_all_time.csv"
            return result, filename
        elif v == "smsdelivery":
            id = campaign_data.get('value')
            name = campaign_data.get('title')
            data = report.sms_delivery_report(report_name="SMS Delivery Statistics",
                                              account_id=f"{account_id}",
                                              account_name=f"{account_name}",
                                              action="Download", report_format="json",
                                              range_period=json.dumps(date_range),
                                              campaign_id=f"{id}")
            data_json = json.loads(data.text)
            result = data_json.get("sms_delivery_statistics")
            filename = f"{path}/{v}_{cur_date_time}_{name}.csv"
            return result, filename

        elif v == "surveyemail":
            id = campaign_data.get('value')
            name = campaign_data.get('title')
            data = report.survey_email_report(report_name="Survey Email Delivery Status Report",
                                              account_id=f"{account_id}",
                                              account_name=f"{account_name}",
                                              action="Download", report_format="json",
                                              range_period=json.dumps(date_range),
                                              campaign_id=id)
            data_json = json.loads(data.text)
            result = data_json.get("survey_delivery_statistics")
            filename = f"{path}/{v}_{cur_date_time}_{name}.csv"
            return result, filename
        elif v == "npsreport":
            data = report.nps_report(report_name="Survey Delivery Statistics",
                                     account_id=f"{account_id}",
                                     account_name=f"{account_name}",
                                     action="Download", report_format="json",
                                     period="All Time")
            data_json = json.loads(data.text)
            result = data_json.get("COPY Default-Tier")
            filename = f"{path}/{v}_all_time.csv"
            return result, filename
        elif v == "tierranking":
            id = campaign_data.get('value')
            name = campaign_data.get('title')
            data = report.ranking_report_tier(report_name="Survey Delivery Statistics",
                                              account_id=f"{account_id}",
                                              account_name=f"{account_name}",
                                              action="Download", report_format="json",
                                              year=config.year, month=config.month_tier,
                                              campaign_id=id)
            data_json = json.loads(data.text)
            result = data_json.get("tier_ranking_details")
            filename = f"{path}/{v}_{config.year}_{config.month}_{name}.csv"
            return result, filename
        elif v == "incompletesurvey":
            data = report.incomplete_survey_report(report_name="Survey Delivery Statistics",
                                                   account_id=f"{account_id}",
                                                   account_name=f"{account_name}",
                                                   action="Download", report_format="json",
                                                   range_period=json.dumps(date_range))
            data_json = json.loads(data.text)
            result = data_json.get("incomplete_survey_details")
            filename = f"{path}/{v}_{cur_date_time}.csv"
            return result, filename
        elif v == "agentranking":
            id = campaign_data.get('value')
            name = campaign_data.get('title')
            data = report.agent_ranking_report(report_name="Agent Ranking",
                                               account_id=f"{account_id}",
                                               action="Download", report_format="json",
                                               year=config.year, month=config.month_tier,
                                               campaign_id=id)
            data_json = json.loads(data.text)
            result = data_json.get("agent_ranking_details")
            filename = f"{path}/{v}_{config.year}_{config.month}_{name}.csv"
            return result, filename
        elif v == "userranking":
            data = report.incomplete_survey_report(report_name="User Ranking",
                                                   account_id=f"{account_id}",
                                                   account_name=f"{account_name}",
                                                   action="Download", report_format="json",
                                                   period=config.period)
            data_json = json.loads(data.text)
            result = data_json.get("user_details")
            filename = f"{path}/{v}_{config.period}.csv"
            return result, filename
    except Exception as e:
        logger.error(f"Failed to generate {k}")
        logger.exception(e)
        return None, None


def convert_into_csv(data, filename, logger):
    logger.info(f"Initialising the file conversion into CSV")
    df = pd.DataFrame.from_dict(data)
    df.to_csv(filename)


def get_user_data(logger):
    try:
        connection = sqlite3.connect('database.db')
        logger.info("Initializing connection for db")
        cursor = connection.cursor()
        data = """SELECT * FROM powertbl;"""
        if data:
            data_values = cursor.execute(data)
            rows = data_values.fetchall()
            for r in rows:
                return r
        else:
            logger.error("This DB doesn't have proper Data")
    except Exception as e:
        logger.error("Can't able to make a proper connection")
        return None
