import config
import constants
import requests
from experience.api.authentication import AuthenticationAPI
from helpers import PowerBI_Reports
from helpers import get_report_data
from helpers import convert_into_csv
from helpers import get_user_data
import json
import crypto
from logger_config import powerBI_log
logger = powerBI_log()



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

    def get_account_data(self):
        url = self.v2_url + "/v2/core/current_user"
        logger.info(f'Trying to get the account_id for the token {self.access_token}')
        data = requests.post(url=url, headers={"Authorization": self.access_token})
        if data:
            data_json = data.json()
            account_data = data_json.get("account_details")
            name = account_data[0].get("name")
            id = account_data[0].get("id")
            return id, name
        else:
            logger.error(f"This token not has a valid account")
            return None, None

    def get_user_details(self):
        result = self.results
        password = crypto.EncryptDecrypt().decryption(result[3],result[2])
        self.authentication = AuthenticationAPI(None, self.v2_url)
        self.access_token = (json.loads(self.authentication.login(result[1], password))).get("auth_token")
        self.reports = result[6]
        self.base_dir = result[7]

    def get_campaign_id(self, account_id):
        logger.info(f'Trying to get the campaign_ids for {account_id}')
        par = {"account_id": {account_id}}
        url = self.report_url + "/fetch/campaign/details"
        campaign_data = requests.get(url=url, params=par, headers={"Authorization": self.access_token})
        if campaign_data:
            return campaign_data.json()
        else:
            logger.error(f"This account has no campaign ids for this {account_id}")
            return []

    def generate_data(self):
        logger.info(f'Initialising the data generation')
        base_dir = self.base_dir
        report = PowerBI_Reports(self.access_token, report_url)
        account_id, account_name= self.get_account_data()
        campaign_data = self.get_campaign_id(account_id)
        try:
            for k, v in self.reports.items():
                if v in ("smsdelivery","surveyemail","tierranking"):
                    logger.info("Initializing report generation with campaign_ids")
                    for d in campaign_data:
                        data, filename = get_report_data(report, v, k, account_id, account_name, logger, base_dir, d)
                        if data and filename:
                            convert_into_csv(data, filename, logger)
                        else:
                            logger.error(f"There is no data on {k} for <{d.get('title')}> campaign")
                            print(f"There is no data on {k} for <{d.get('title')}> campaign")
                else:
                    logger.info("Initializing report generation without campaign_ids")
                    data, filename = get_report_data(report, v, k, account_id, account_name, logger, base_dir)
                    if data and filename:
                        convert_into_csv(data, filename, logger)
                    else:
                        logger.error(f"There is no data for {k}")
                        print(f"There is no data for {k}")
        except Exception as e:
            logger.error(f"Unable to generate report data")
            logger.exception(e)



if __name__ == "__main__":
    v2_url = constants.v2_api.get(config.env)
    report_url = constants.report_api.get(config.env)
    powerbi = PowerBIDataIngestion(v2_url, report_url)
    powerbi.generate_data()
