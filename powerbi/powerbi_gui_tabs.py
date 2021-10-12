from datetime import datetime
from tkcalendar import dateentry
import tkinter as tk              
from tkinter import ttk
TK_SILENCE_DEPRECATION=1
from tkinter import *
from tkcalendar import *
from tkinter import filedialog
import sqlite3
import tkinter.messagebox as msgbox
import json

from powerbi.power_bi_integration import PowerBIDataIngestion
from powerbi import constants
from powerbi import crypto


# tkinter obj configs
root = tk.Tk()
root.title("Experience.com")
root.geometry("600x600")
root.resizable(False, False)

# tab widgets
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Reports scheduler')
tabControl.add(tab2, text ='Custom report generation')
tabControl.pack(fill='both', expand=1)
  
# variables for reports
error_window = False

report_path = ""

start_date = StringVar()
end_date = StringVar()

username = StringVar()
password = StringVar()

survey_results = IntVar()
reviews_management = IntVar()
publish_history = IntVar()
hierarchy_details = IntVar()
nps_trend = IntVar()
account_statistics = IntVar()
sms_delivery = IntVar()
survey_email = IntVar()
verified_users = IntVar()
nps = IntVar()
ranking_tier = IntVar()
incomplete_survey = IntVar()
survey_statistics = IntVar()

sandbox = IntVar()
production = IntVar()

survey_results_scheduler = IntVar()
reviews_management_scheduler = IntVar()
publish_history_scheduler = IntVar()
hierarchy_details_scheduler = IntVar()
nps_trend_scheduler = IntVar()
account_statistics_scheduler = IntVar()
sms_delivery_scheduler = IntVar()
survey_email_scheduler = IntVar()
verified_users_scheduler = IntVar()
nps_scheduler = IntVar()
ranking_tier_scheduler = IntVar()
incomplete_survey_scheduler = IntVar()
survey_statistics_scheduler = IntVar()

sandbox_scheduler = IntVar()
production_scheduler = IntVar()

report_path_scheduler = ''

def database():
    conn = sqlite3.connect('database.db')
    connection = conn.cursor()
    connection.execute("CREATE TABLE IF NOT EXISTS powertbl(id integer primary key autoincrement, name TEXT, password TEXT, start_date TEXT, end_date TEXT, reports TEXT, report_type TEXT, environment TEXT, report_path TEXT, api_key TEXT, created_at DATETIME NOT NULL)")
    conn.commit()

database()


# def report_type_check():
#     conn = sqlite3.connect('database.db')
#     connection = conn.cursor()
#     report_type = connection.execute("SELECT report_type from powertbl")
#     return report_type


def select_tab():
    tabControl.select(1)


def delete(window):
    global error_window
    window.destroy()
    error_window = False


def success():
    msgbox.showinfo(title='success!', message='Thank You, if provided detail are valid, requested report will be generated')
    root.destroy()


def error_window_screen(dimension, text_field):
    global error_window
    error_window = True
    error_window = Toplevel(root)
    error_window.attributes('-topmost', 'true')
    error_window.geometry(dimension)
    error_window.title("Warning!")
    Label(error_window, text=text_field, fg="red").pack()
    Button(error_window, text="OK", command= lambda: delete(error_window)).pack()


def error_window_screen_username_password(dimension, text_field):
    global error_window
    error_window = True
    error_window = Toplevel(root)
    error_window.attributes('-topmost', 'true')
    error_window.geometry(dimension)
    error_window.title("Warning!")
    tabControl.select(0)
    Label(error_window, text=text_field, fg="red").pack()
    Button(error_window, text="OK", command= lambda: delete(error_window)).pack()


def open_dialog():
    global report_path
    if report_path != '':
        report_path = ''
    report_path =  filedialog.askdirectory(initialdir='/', title='select the location for report to be downloaded')
    Label(tab1, text=f"reports will reside in directory: {report_path}", foreground="red", font=constants.WIDGET_FONT_COLOR).grid(row=16, sticky=constants.WIDGET_REGION)
    # Label(tab2, text=f"reports will reside in directory: {report_path}", foreground="red", font=constants.WIDGET_FONT_COLOR).grid(row=16, sticky=constants.WIDGET_REGION)

def open_dialog_scheduler():
    global report_path_scheduler
    if report_path_scheduler != '':
        report_path_scheduler = ''
    report_path_scheduler =  filedialog.askdirectory(initialdir='/', title='select the location for report to be downloaded')
    Label(tab1, text=f"reports will reside in directory: {report_path_scheduler}", foreground="red", font=constants.WIDGET_FONT_COLOR).grid(row=16, sticky=constants.WIDGET_REGION)



def open_dialog_custom():
    global report_path
    if report_path != '':
        report_path = ""
    report_path =  filedialog.askdirectory(initialdir='/', title='select the location for report to be downloaded')
    Label(tab2, text=f"reports will reside in directory: {report_path}", foreground="red", font=constants.WIDGET_FONT_COLOR).grid(row=16, sticky=constants.WIDGET_REGION)


def get_start_date():
    return start_date.get()


def get_end_date():
    return end_date.get()


def register_user():
    # import pdb; pdb.set_trace()
    report_type = ""
    """after successfull verification saving the user"""
    global error_window, username, password, survey_results, reviews_management, survey_statistics, publish_history, hierarchy_details
    global verified_users, nps_trend, account_statistics, sms_delivery, survey_email, nps, ranking_tier, incomplete_survey, sandbox, production

    global survey_results_scheduler, reviews_management_scheduler, survey_statistics_scheduler, publish_history_scheduler, hierarchy_details_scheduler
    global verified_users_scheduler, nps_trend_scheduler, account_statistics_scheduler, sms_delivery_scheduler, survey_email_scheduler
    global nps_trend_scheduler, ranking_tier_scheduler, incomplete_survey_scheduler, sandbox, production_scheduler

    username_text = username.get()
    password_text = password.get()

    reports_check = [survey_results.get(), reviews_management.get(), survey_statistics.get(), publish_history.get(), hierarchy_details.get(), verified_users.get(),
                     nps_trend.get(), account_statistics.get(), sms_delivery.get(), survey_email.get(), nps.get(), ranking_tier.get(), incomplete_survey.get()]
    
    reports_check_scheduler = [survey_results_scheduler.get(), reviews_management_scheduler.get(), survey_statistics_scheduler.get(),
                               publish_history_scheduler.get(), hierarchy_details_scheduler.get(), verified_users_scheduler.get(),
                               nps_trend_scheduler.get(), account_statistics_scheduler.get(), sms_delivery_scheduler.get(), 
                               survey_email_scheduler.get(), nps.get(), ranking_tier_scheduler.get(), incomplete_survey_scheduler.get()]
    
    environment_check = [sandbox.get(), production.get()]
    environment_check_schedulder = [sandbox_scheduler.get(), production_scheduler.get()]
    

    if not username_text or not password_text:
        # import pdb; pdb.set_trace()
        if not error_window:
            # width and height for err win
            error_window_screen_username_password("280x100", "username and password fields are required.")
    elif not any(reports_check) and not any(reports_check_scheduler):
        if not error_window:
            error_window_screen("220x100", "please select a report.")
    elif not any(environment_check) and not any(environment_check_schedulder):
        if not error_window:
            error_window_screen("300x100", "please select a environment to generate report.")
    elif environment_check[0] and environment_check[1]:
        if not error_window:
            error_window_screen("330x100", "please select only one environment to generate report.")
    elif environment_check_schedulder[0] and environment_check_schedulder[1]:
        if not error_window:
            error_window_screen("330x100", "please select only one environment to generate report.")
    elif not report_path and not report_path_scheduler:
        if not error_window:
            error_window_screen("300x100", "please select a path to download report.")
    else:
        if any(reports_check):
            report_type = "custom"
        if any(reports_check_scheduler):
            report_type = "scheduler"
        ingest_data(report_type)


def ingest_data(report_type):
    # import pdb; pdb.set_trace()
    """adding user details to the database"""
    global report_path, report_path_scheduler
    total_reports = {}
    environment = ""
    total_reports_scheduler = {}
    environment_scheduler = ""

    if survey_results.get():
        total_reports["survey_results_report"] = "surveyresults"
    if reviews_management.get():
        total_reports["reviews_management_report"] = "reviewsmanagement"
    if survey_statistics.get():
        total_reports["survey_statistics_report"] = "surveystatistics"
    if publish_history.get():
        total_reports["publish_history_report"] = "publishhistory"
    if hierarchy_details.get():
        total_reports["hierarchy_details_report"] = "hierarchydetails"
    if verified_users.get():
        total_reports["verified_users_report"] = "verifiedusers"
    if nps_trend.get():
        total_reports["nps_trend_report"] = "npstrend"
    if account_statistics.get():
        total_reports["account_statistics_report"] = "accountstatistics"
    if sms_delivery.get():
        total_reports["sms_delivery_report"] = "smsdelivery"
    if survey_email.get():
        total_reports["survey_email_report"] = "surveyemail"
    if nps.get():
        total_reports["nps_report"] = "npsreport"
    if ranking_tier.get():
        total_reports["ranking_report_tier"] = "tierranking"
    if incomplete_survey.get():
        total_reports["incomplete_survey_report"] = "incompletesurvey"
    
    if survey_results_scheduler.get():
        total_reports_scheduler["survey_results_report"] = "surveyresults"
    if reviews_management_scheduler.get():
        total_reports_scheduler["reviews_management_report"] = "reviewsmanagement"
    if survey_statistics_scheduler.get():
        total_reports_scheduler["survey_statistics_report"] = "surveystatistics"
    if publish_history_scheduler.get():
        total_reports_scheduler["publish_history_report"] = "publishhistory"
    if hierarchy_details_scheduler.get():
        total_reports_scheduler["hierarchy_details_report"] = "hierarchydetails"
    if verified_users_scheduler.get():
        total_reports_scheduler["verified_users_report"] = "verifiedusers"
    if nps_trend_scheduler.get():
        total_reports_scheduler["nps_trend_report"] = "npstrend"
    if account_statistics_scheduler.get():
        total_reports_scheduler["account_statistics_report"] = "accountstatistics"
    if sms_delivery_scheduler.get():
        total_reports_scheduler["sms_delivery_report"] = "smsdelivery"
    if survey_email_scheduler.get():
        total_reports_scheduler["survey_email_report"] = "surveyemail"
    if nps_trend_scheduler.get():
        total_reports_scheduler["nps_report"] = "npsreport"
    if ranking_tier_scheduler.get():
        total_reports_scheduler["ranking_report_tier"] = "tierranking"
    if incomplete_survey_scheduler.get():
        total_reports_scheduler["incomplete_survey_report"] = "incompletesurvey"

    
    if sandbox.get():
        environment =  "SANDBOX"
    if production.get():
        environment = "PRODUCTION"
    
    if sandbox_scheduler.get():
        environment_scheduler =  "SANDBOX"
    if production_scheduler.get():
        environment_scheduler = "PRODUCTION"

    try:
        conn = sqlite3.connect("database.db")
        connection = conn.cursor()
        utc_date_time = datetime.utcnow()

        start_date = get_start_date()
        end_date = get_end_date()
        current_date = datetime.strftime(utc_date_time, "%Y-%m-%d")
        created_at = datetime.strftime(utc_date_time, "%Y-%m-%d %H:%M:%S")
        start_date = start_date if start_date else current_date
        end_date = end_date if end_date else current_date
        encryption_obj = crypto.EncryptDecrypt()
        encryped_password, decrypt_key  = encryption_obj.encryption(password.get())
        if report_type == "custom":
            reports_data = (None, username.get(), str(encryped_password, 'UTF-8'), str(decrypt_key, 'UTF-8'), start_date, end_date, total_reports, report_path, created_at)
            try:
                print('Report generation starts...')
                # powerbi_ingestion = PowerBIDataIngestion(constants.v2_api.get(environment), constants.report_api.get(environment), reports_data)
                # powerbi_ingestion.generate_data()
            except Exception as err:
                print(str(err))
            finally:
                connection.execute('INSERT INTO powertbl(name, password, start_date, end_date, reports, environment, report_type, report_path, api_key, created_at) VALUES(?,?,?,?,?,?,?,?,?,?)', (username.get(), encryped_password, start_date, end_date, json.dumps(total_reports), environment, report_type, report_path, decrypt_key, created_at))
                conn.commit()
                success()
        else:
            connection.execute('INSERT INTO powertbl(name, password, start_date, end_date, reports, environment, report_type, report_path, api_key, created_at) VALUES(?,?,?,?,?,?,?,?,?,?)', (username.get(), encryped_password, start_date, end_date, json.dumps(total_reports_scheduler), environment_scheduler, report_type, report_path_scheduler, decrypt_key, created_at))
            conn.commit()
            success()
    except Exception as err:
        print(str(err))

# design layout
Label(tab1, text="Username *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=0, sticky=constants.WIDGET_REGION)
Entry(tab1, textvariable=username, bg="lightgray", width=25).grid(row=1, sticky=constants.WIDGET_REGION)
Label(tab1, text= "Password *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=2, sticky=constants.WIDGET_REGION)
Entry(tab1, textvariable=password, bg="lightgray", width=25, show="*").grid(row=3, sticky=constants.WIDGET_REGION)
Label(tab1, text= "Select report/reports *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=4, sticky=constants.WIDGET_REGION)
config_check = Checkbutton(tab1, text = "Survey Results", variable=survey_results_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=5, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Reviews_Management", variable=reviews_management_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=5, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Publish History", variable=publish_history_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=6, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Hierarchy Details", variable=hierarchy_details_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=6, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "NPS Trend", variable=nps_trend_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=7, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Account Statistics", variable=account_statistics_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=7, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "SMS Delivery", variable=sms_delivery_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=8, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Survey Email", variable=survey_email_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=8, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Verified Users", variable=verified_users_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=9, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "NPS", variable=nps_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=9, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Ranking Tier", variable=ranking_tier_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=10, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Incomplete Survey", variable=incomplete_survey_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=10, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Survey Statistics", variable=survey_statistics_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=11, sticky=constants.WIDGET_REGION)
Label(tab1, text="Select Environment *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=12, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Sandbox", variable=sandbox_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=13, sticky=constants.WIDGET_REGION)
Checkbutton(tab1, text = "Production", variable=production_scheduler, font=constants.WIDGET_FONT_COLOR).grid(row=13, column=1, sticky=constants.WIDGET_REGION)
Button(tab1, text="Select path", width=20, font=constants.WIDGET_FONT_COLOR, command=open_dialog_scheduler).grid(row=15, sticky=constants.WIDGET_REGION)
Button(tab1, text="Submit", width="18", bg="white", highlightbackground="#98fb98", command=register_user, font=constants.WIDGET_FONT_COLOR).grid(row=17, sticky=constants.WIDGET_REGION)
# Button(tab1, text='Switch to custom reports', command=select_tab, font=constants.WIDGET_FONT_COLOR).grid(row=15, sticky=constants.WIDGET_REGION)

Label(tab2, text= "Select report/reports *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Survey Results", variable=survey_results, font=constants.WIDGET_FONT_COLOR).grid(row=2, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Reviews_Management", variable=reviews_management, font=constants.WIDGET_FONT_COLOR).grid(row=2, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Publish History", variable=publish_history, font=constants.WIDGET_FONT_COLOR).grid(row=3, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Hierarchy Details", variable=hierarchy_details, font=constants.WIDGET_FONT_COLOR).grid(row=3, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "NPS Trend", variable=nps_trend, font=constants.WIDGET_FONT_COLOR).grid(row=4, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Account Statistics", variable=account_statistics, font=constants.WIDGET_FONT_COLOR).grid(row=4, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "SMS Delivery", variable=sms_delivery, font=constants.WIDGET_FONT_COLOR).grid(row=5, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Survey Email", variable=survey_email, font=constants.WIDGET_FONT_COLOR).grid(row=5, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Verified Users", variable=verified_users, font=constants.WIDGET_FONT_COLOR).grid(row=6, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "NPS", variable=nps, font=constants.WIDGET_FONT_COLOR).grid(row=6, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Ranking Tier", variable=ranking_tier, font=constants.WIDGET_FONT_COLOR).grid(row=7, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Incomplete Survey", variable=incomplete_survey, font=constants.WIDGET_FONT_COLOR).grid(row=7, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Survey Statistics", variable=survey_statistics, font=constants.WIDGET_FONT_COLOR).grid(row=8, sticky=constants.WIDGET_REGION)
# Label(tab2, foreground="red", text="Note: If start and end dates are not selected, present date will be taken.").grid(row=13, sticky=constants.WIDGET_REGION)
Label(tab2, text= "Look back report start date", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=9, sticky=constants.WIDGET_REGION)
DateEntry(tab2, width= 16, background= constants.FOREGOUND_COLOR_BLUE, textvariable=start_date, foreground= constants.FOREGOUND_COLOR_DARK, bd=2).grid(row=10, sticky=constants.WIDGET_REGION)
Label(tab2, text= "Look back report end date", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=11, sticky=constants.WIDGET_REGION)
DateEntry(tab2, width= 16, background= constants.FOREGOUND_COLOR_BLUE, textvariable=end_date, foreground= constants.FOREGOUND_COLOR_DARK, bd=2).grid(row=12, sticky=constants.WIDGET_REGION)
Label(tab2, text="Select Environment *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=13, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Sandbox", variable=sandbox, font=constants.WIDGET_FONT_COLOR).grid(row=14, sticky=constants.WIDGET_REGION)
Checkbutton(tab2, text = "Production", variable=production, font=constants.WIDGET_FONT_COLOR).grid(row=14, column=1, sticky=constants.WIDGET_REGION)
Button(tab2, text="Select path", width=20, font=constants.WIDGET_FONT_COLOR, command=open_dialog_custom).grid(row=15, sticky=constants.WIDGET_REGION)
Button(tab2, text="Generate report", width="18", bg="white", highlightbackground="#98fb98", command=register_user, font=constants.WIDGET_FONT_COLOR).grid(row=17, sticky=constants.WIDGET_REGION)
  
root.mainloop()
