from experience.api.reports import ReportsAPI


class PowerBI_Reports(ReportsAPI):

    def __init__(self, access_token, base_url):
        super().__init__(access_token, base_url)







def get_report_data(report, v):
    if v=='surveyresults':
        data = report.survey_results_report()