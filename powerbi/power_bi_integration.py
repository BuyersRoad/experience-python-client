import config
import constants
from experience.api.authentication import AuthenticationAPI
from helpers import PowerBI_Reports
from helpers import get_report_data





class PowerBI_Data_ingestion:


    def __init__(self, v2_url, report_url):
        self.v2_url = v2_url
        self.report_url = report_url
        self.authentication = AuthenticationAPI(None, self.v2_url)
        self.access_token = self.authentication.login(config.username, config.password)

    def generate_data(self):
        print("access_token", self.access_token)
        print(type(self.access_token))
        print("reporturl", report_url)
        report = PowerBI_Reports(self.access_token.get('auth_token'), report_url)
        for k,v in constants.reports_names.items():
            data = get_report_data(report, v)
            print(data)




















if __name__=="__main__":
    v2_url = constants.v2_api.get(config.env)
    report_url = constants.report_api.get(config.env)
    powerbi = PowerBI_Data_ingestion(v2_url,report_url)
    powerbi.generate_data()


