import config
import constants
import requests
from experience.api.authentication import AuthenticationAPI
from helpers import PowerBI_Reports
from helpers import get_report_data
from helpers import convert_into_csv
from helpers import get_user_data
import json



class PowerBIDataIngestion:

    def __init__(self, v2_url, report_url,username = None):
        self.v2_url = v2_url
        self.report_url = report_url
        self.campaign_ids = []
        if username is None:
            self.results = get_user_data()
        else:
            self.results = username
        self.get_user_details()


    def get_account_id(self):
        url = self.v2_url + "/v2/core/current_user"
        data = requests.post(url=url, headers={"Authorization": self.access_token})
        if data:
            data_json = data.json()
            account_id = data_json.get("account_id")
            return account_id[0]
        else:
            return None

    def get_user_details(self):
        result = self.results
        self.authentication = AuthenticationAPI(None, self.v2_url)
        self.access_token = (json.loads(self.authentication.login(result[0], result[1]))).get("auth_token")
        self.reports = result[5]

    def get_campaign_id(self, account_id):
        par = {"account_id": {account_id}}
        url = self.report_url + "/fetch/campaign/details"
        campaign_data = requests.get(url=url, params=par, headers={"Authorization": self.access_token})
        if campaign_data:
            return campaign_data.json()
        else:
            return None

    def generate_data(self):
        report = PowerBI_Reports(self.access_token, report_url)
        v2_report = PowerBI_Reports(self.access_token, v2_url)
        account_id = self.get_account_id()
        campaign_data = self.get_campaign_id(account_id)
        try:
            for k, v in self.reports.items():
                if v in ("smsdelivery","surveyemail","tierranking"):
                    for d in campaign_data:
                        data, filename = get_report_data(report, v, k, account_id, d)
                        if data and filename:
                            convert_into_csv(data, filename)
                        else:
                            print(f"There is no data on {k} for <{d.get('title')}> campaign")
                else:
                    data, filename = get_report_data(report, v, k, account_id)
                    if data and filename:
                        convert_into_csv(data, filename)
                    else:
                        print(f"There is no data for {k}")
            # for k, v in constants.v2_reports.items():
            #     data, filename = get_report_data(v2_report, v, k)
            #     if data and filename:
            #         convert_into_csv(data, filename)
            #     else:
            #         print(f"There is no data for {k}")
        except Exception as e:
            print(e)
            raise



if __name__ == "__main__":
    v2_url = constants.v2_api.get(config.env)
    report_url = constants.report_api.get(config.env)
    powerbi = PowerBIDataIngestion(v2_url, report_url)
    powerbi.generate_data()
