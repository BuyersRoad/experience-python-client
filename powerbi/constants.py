v2_api = {
    'DEV': 'https://api.devtest.experience.com',
    'PREPROD': 'https://api.preprod.experience.com',
    'PROD': 'https://api.experience.com',
    'SANDBOX': 'https://api.preprod.experience.com'
}

report_api = {
    'DEV': "https://reports.devtest.experience.com",
    'PREPROD': "https://reports.preprod.experience.com",
    "PROD": "https://reports.experience.com",
    "SANDBOX": "https://reports.preprod.experience.com"
}


reports_names = {"survey_results_report": "surveyresults",
                 "reviews_management_report": "reviewsmanagement",
                 "survey_statistics_report": "surveystatistics",
                 "publish_history_report": "publishhistory",
                 "hierarchy_details_report": "hierarchydetails",
                 "verified_users_report": "verifiedusers",
                 "nps_trend_report": "npstrend",
                 "account_statistics_report": "accountstatistics",
                 "sms_delivery_report": "smsdelivery",
                 "survey_email_report": "surveyemail",
                 "nps_report": "npsreport",
                 "ranking_report_tier": "tierranking",
                 "incomplete_survey_report": "incompletesurvey"}

v2_reports = {"mismatch_transactions_report": "mismatch",
              "uncollected_transactions_report": "uncollected",
              "user_ranking_report": "userranking",
              "company_user_report": "companyuser"}

WIDGET_FONT_COLOR = ("times new roman", 15, "bold")
WIDGET_REGION = 'w'
FOREGOUND_COLOR_BLUE = "DodgerBlue"
FOREGOUND_COLOR_DARK = "darkblue"
PS1_SCRIPT_PATH_DAILY = ".\pshell_daily.ps1"
PS1_SCRIPT_PATH_MONTHLY = ".\pshell_monthly.ps1"
POWERBI_REPORT_SCRIPT_PATH_DAILY = "/power_bi_integration.py"
POWERBI_REPORT_SCRIPT_PATH_MONTHLY = "/power_bi_integration.py"
