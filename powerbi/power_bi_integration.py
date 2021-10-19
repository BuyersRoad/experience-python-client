import constants
import requests
from experience.api.authentication import AuthenticationAPI
from helpers import PowerBI_Reports
from helpers import get_report_data
from helpers import convert_into_csv
from helpers import get_user_data
from helpers import get_date_range
import json
import crypto
from logger_config import powerBI_log

logger = powerBI_log()


class PowerBIDataIngestion:

    def __init__(self, username=None):
        self.campaign_ids = []
        if username is None:
            self.results = get_user_data(logger)
        else:
            self.results = username
        self.v2_url = constants.v2_api.get(self.results[10])
        self.report_url = constants.report_api.get(self.results[10])
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

    def get_access_token(self, user, passwd):
        token = (json.loads(self.authentication.login(user, passwd))).get("auth_token")
        return token

    def get_user_details(self):
        result = self.results
        password = crypto.EncryptDecrypt().decryption(result[3], result[2])
        self.authentication = AuthenticationAPI(None, self.v2_url)
        self.access_token = self.get_access_token(result[1], password)
        self.report_type = result[9]
        if self.report_type == "scheduler":
            self.reports = json.loads(result[6])
        else:
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
        report = PowerBI_Reports(self.access_token, self.report_url)
        account_id, account_name = self.get_account_data()
        campaign_data = self.get_campaign_id(account_id)
        result = self.results
        start_date = result[4]
        end_date = result[5]
        date_period = get_date_range(start_date, end_date)
        try:
            for k, v in self.reports.items():
                if v in ("smsdelivery", "surveyemail"):
                    logger.info("Initializing report generation with campaign_ids")
                    for d in campaign_data:
                        data, filename = get_report_data(report, v, k, account_id, account_name, logger, result,
                                                         campaign_data=d)
                        if data and filename:
                            convert_into_csv(data, filename, logger)
                        else:
                            logger.error(f"There is no data on {k} for <{d.get('title')}> campaign")
                            print(f"There is no data on {k} for <{d.get('title')}> campaign")
                elif v in ("tierranking", "agentranking"):
                    logger.info(f"Initializing report generation with campaign_ids and specific Month period")
                    for month_year in date_period:
                        year = month_year.get("year")
                        month = month_year.get("month")
                        for d in campaign_data:
                            data, filename = get_report_data(report, v, k, account_id, account_name, logger, result,
                                                             campaign_data=d, month=month, year=year)
                            if data and filename:
                                convert_into_csv(data, filename, logger)

                            else:
                                logger.error(
                                    f"There is no data on {k} for <{d.get('title')}> campaign on {month} {year}")
                                print(f"There is no data on {k} for <{d.get('title')}> campaign")
                elif v in ("hierarchydetails", "npstrend","userranking"):
                    logger.info(f"Initializing report generation with specific month period only")
                    for month_year in date_period:
                        year = month_year.get("year")
                        month = month_year.get("month")
                        data, filename = get_report_data(report, v, k, account_id, account_name, logger, result,
                                                         month=month, year=year)
                        if data and filename:
                            convert_into_csv(data, filename, logger)
                        else:
                            logger.error(f"There is no data for {k} on {month} {year}")
                            print(f"There is no data for {k}")
                else:
                    logger.info("Initializing report generation without campaign_ids and specific Months")
                    data, filename = get_report_data(report, v, k, account_id, account_name, logger, result)
                    if data and filename:
                        convert_into_csv(data, filename, logger)
                    else:
                        logger.error(f"There is no data for {k}")
                        print(f"There is no data for {k}")
        except Exception as e:
            logger.error(f"Unable to generate report data")
            logger.exception(e)


if __name__ == "__main__":
    powerbi = PowerBIDataIngestion()
    powerbi.generate_data()
