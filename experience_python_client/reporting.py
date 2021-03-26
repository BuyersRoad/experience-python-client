import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from experience_python_client.api_consume import Report, Login
from experience_python_client.constants import access_token

authentication = Login()
report = Report()

login = authentication.login(username='', password='')
current_user_details = report.current_user_details(access_token=access_token)
activity_feed = report.activity_feed(access_token=access_token, id='1892', page='3')
tier_details = report.tier_details(access_token=access_token, org_id=4, account_id=1892)
agent_ranking_report = report.agent_ranking_report(access_token=access_token, account_id=1892, campaign_id=760,
                                                   year=2021, month='april', report_format='json')
hierarchy_details_report = report.hierarchy_details_report(access_token=access_token, account_id=1892,
                                                           report_format='json', period='today')
incomplete_survey_report = report.incomplete_survey_report(access_token=access_token, account_id=1892,
                                                           report_format='json',
                                                           range_period=['2021-02-01', '2021-02-11'], campaign_id=760)
nps_report = report.nps_report(access_token=access_token, account_id=1892, report_format='json', period='today')
publish_history_report = report.publish_history_report(access_token=access_token, account_id=1892, report_format='json')
reviews_management_report = report.reviews_management_report(access_token=access_token, account_id=1892,
                                                             report_format='json',
                                                             range_period=['2021-02-01', '2021-02-11'])
survey_results_report = report.survey_results_report(access_token=access_token, account_id=1892, report_format='json',
                                                     range_period=['2021-02-01', '2021-02-05'])
survey_statistics_report = report.survey_statistics_report(access_token=access_token, account_id=1892,
                                                           report_format='json',
                                                           range_period=['2021-02-01', '2021-02-05'])
ranking_report_tier = report.ranking_report_tier(access_token=access_token, account_id=1892, campaign_id=760, year=2021,
                                                 month='march', report_format='json')
user_details_report = report.user_details_report(access_token=access_token, account_id=1892,
                                                 report_format='json', period='today')
verified_users_report = report.verified_users_report(access_token=access_token, account_id=1892, report_format='json')
agent_details = report.agent_details(access_token=access_token, org_id=10087, account_id=1892)
campaign_details = report.campaign_details(access_token=access_token, account_id=1892)
