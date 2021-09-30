import config
import constants
from experience.api.authentication import AuthenticationAPI
from helpers import PowerBI_Reports
from helpers import get_report_data
from helpers import convert_into_csv
import json


class PowerBI_Data_ingestion:

    def __init__(self, v2_url, report_url):
        self.v2_url = v2_url
        self.report_url = report_url
        self.authentication = AuthenticationAPI(None, self.v2_url)
        self.access_token = self.authentication.login(config.username, config.password)

    def generate_data(self):
        token_json = (json.loads(self.access_token))
        report = PowerBI_Reports(token_json.get('auth_token'), report_url)
        v2_report = PowerBI_Reports(token_json.get('auth_token'), v2_url)
        try:
            for k, v in constants.reports_names.items():
                data, filename = get_report_data(report, v)
                if data and filename:
                    convert_into_csv(data, filename)
                else:
                    print(f"There is no data for {k}")
            for k, v in constants.v2_reports.items():
                data = get_report_data(v2_report, v)
                if data and filename:
                    convert_into_csv(data, filename)
                else:
                    print(f"There is no data for {k}")
        except Exception as e:
            print(e)
            raise



if __name__ == "__main__":
    v2_url = constants.v2_api.get(config.env)
    report_url = constants.report_api.get(config.env)
    powerbi = PowerBI_Data_ingestion(v2_url, report_url)
    powerbi.generate_data()
