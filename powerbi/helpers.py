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
    start_date = (today_date - timedelta(days=date)).strftime("%Y-%m-%d")
    return [start_date, end_date]


def get_report_data(report, v):
    date_range = get_date_range(config.data_range)
    cur_date_time = ("{:%Y_%m_%d}".format(dt.now()))
    if v == "surveyresults":
        data = report.survey_results_report(account_id=config.account_id, report_format='json',
                                            range_period=json.dumps(date_range))
        data_json = json.loads(data.text)
        result = data_json.get("survey_results")
        filename = f"{v}_{cur_date_time}.csv"
        return result, filename
    elif v == "reviewsmanagement":
        data = report.reviews_management_report(account_id=config.account_id, report_format='json',
                                                range_period=json.dumps(date_range))
        data_json = json.loads(data.text)
        result = data_json.get("reviews_management_tier_details")
        filename = f"{v}_{cur_date_time}.csv"
        return result, filename
    elif v == "surveystatistics":
        data = report.survey_statistics_report(account_id=config.account_id, report_format='json',
                                               range_period=json.dumps(date_range))
        data_json = json.loads(data.text)
        filename = f"{v}_{cur_date_time}.csv"
        return data_json, filename
    elif v == "publishhistory":
        data = report.publish_history_report(report_name="Publish History",
                                             account_id=config.account_id,
                                             account_name=config.account_name,
                                             action="Download", report_format="json",
                                             tier_data=[
                                                 {"label": "All Tier", "value": config.account_id}])
        data_json = json.loads(data.text)
        result = data_json.get("agent_details")
        filename = f"{v}_all_time.csv"
        return result, filename
    elif v == "hierarchydetails":
        data = report.hierarchy_details_report(report_name="Hierarchy Details",
                                               account_id=config.account_id,
                                               account_name=config.account_name,
                                               action="Download", report_format="json", period=config.month)
        data_json = json.loads(data.text)
        result = data_json.get("hierarchy_user_details")
        filename = f"{v}_{config.month}.csv"
        return result, filename
    elif v == "verifiedusers":
        data = report.verified_users_report(report_name="Verified Users",
                                            account_id=config.account_id,
                                            account_name=config.account_name,
                                            action="Download", report_format="json",
                                            tier_data=[{"label": "All Tier", "value": config.account_id}])
        data_json = json.loads(data.text)
        result = data_json.get("verified_user_details")
        filename = f"{v}_all_time.csv"
        return result, filename
    elif v == "npstrend":
        data = report.nps_trend_report(report_name="NPS Trend Report",
                                       account_id=config.account_id,
                                       account_name=config.account_name,
                                       action="Download", report_format="json", period=config.month)
        data_json = json.loads(data.text)
        result = data_json.get("loading test-Tier")
        filename = f"{v}_{config.month}.csv"
        return result, filename
    elif v == "accountstatistics":
        data = report.account_statistics_report(report_name="Account Statistics Report",
                                                account_id=config.account_id,
                                                account_name=config.account_name,
                                                action="Download", report_format="json")
        data_json = json.loads(data.text)
        result = data_json.get("accounts")
        filename = f"{v}_all_time.csv"
        return result, filename
    elif v == "smsdelivery":
        data = report.sms_delivery_report(report_name="SMS Delivery Statistics",
                                          account_id=config.account_id,
                                          account_name=config.account_name,
                                          action="Download", report_format="json",
                                          range_period=json.dumps(date_range),
                                          campaign_id=config.campaign_id)
        data_json = json.loads(data.text)
        result = data_json.get("sms_delivery_statistics")
        filename = f"{v}_{cur_date_time}.csv"
        return result, filename
    elif v == "surveyemail":
        data = report.survey_email_report(report_name="Survey Email Delivery Status Report",
                                          account_id=config.account_id,
                                          account_name=config.account_name,
                                          action="Download", report_format="json",
                                          range_period=json.dumps(date_range),
                                          campaign_id=config.campaign_id)
        data_json = json.loads(data.text)
        result = data_json.get("survey_delivery_statistics")
        filename = f"{v}_{cur_date_time}.csv"
        return result, filename
    elif v == "npsreport":
        data = report.nps_report(report_name="Survey Delivery Statistics",
                                 account_id=config.account_id,
                                 account_name=config.account_name,
                                 action="Download", report_format="json",
                                 period="All Time")
        data_json = json.loads(data.text)
        result = data_json.get("API call test-Tier")
        filename = f"{v}_all_time.csv"
        return result, filename
    elif v == "tierranking":
        data = report.ranking_report_tier(report_name="Survey Delivery Statistics",
                                          account_id=config.account_id,
                                          account_name=config.account_name,
                                          action="Download", report_format="json",
                                          year=config.year, month=config.month,
                                          campaign_id=config.campaign_id)
        data_json = json.loads(data.text)
        result = data_json.get("tier_ranking_details")
        filename = f"{v}_{config.year}_{config.month}.csv"
        return result, filename
    elif v == "incompletesurvey":
        data = report.incomplete_survey_report(report_name="Survey Delivery Statistics",
                                               account_id=config.account_id,
                                               account_name=config.account_name,
                                               action="Download", report_format="json",
                                               campaign_id=config.campaign_id,
                                               range_period=json.dumps(date_range))
        data_json = json.loads(data.text)
        result = data_json.get("incomplete_survey_details")
        filename = f"{v}_{cur_date_time}.csv"
        return result, filename


def convert_into_csv(data, filename):
    df = pd.DataFrame.from_dict(data)
    df.to_csv(filename)
