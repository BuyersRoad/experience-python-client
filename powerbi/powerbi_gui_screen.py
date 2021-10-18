from logging import basicConfig
from tkinter import *
from tkcalendar import *
from powerbi import constants
from tkinter import filedialog
import tkinter.messagebox as msgbox
import sqlite3
import json
from powerbi.power_bi_integration import PowerBIDataIngestion
from experience.api.authentication import AuthenticationAPI
from powerbi import crypto
from datetime import datetime, time
import time as t
import subprocess, sys
import random

from powerbi.logger_config import gui_log
log = gui_log()

root = Tk()
# root.geometry("400x300")
root.resizable(False, False)
root.title("User Details")


# StringVars
username = StringVar()
password = StringVar()
error_window = False
sandbox = IntVar()
production = IntVar()

# Label Widget
user_label = Label(root, text="Username *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR)
pass_label = Label(root, text="Password *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR)
env_label = Label(root, text="Select Environment *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR)
check_sand = Checkbutton(root, text = "Sandbox", variable=sandbox, font=constants.WIDGET_FONT_COLOR)
check_prod = Checkbutton(root, text = "Production", variable=production, font=constants.WIDGET_FONT_COLOR)

user_label.grid(row=0, column=0, sticky=constants.WIDGET_REGION)
pass_label.grid(row=2, column=0, sticky=constants.WIDGET_REGION)
env_label.grid(row=5, sticky=constants.WIDGET_REGION)
check_sand.grid(row=6, column=0, sticky=constants.WIDGET_REGION)
check_prod.grid(row=6, column=1, sticky=constants.WIDGET_REGION)

bad_pass = Label(root, text="incorrect username or password", foreground="red")
no_env = Label(root, text="please select one environment", foreground="red")

# Entry fields
username_obj = Entry(root, textvariable=username, bg="lightgray", width=25)
password_obj = Entry(root, show='*', textvariable=password, bg="lightgray", width=25)
username_obj.grid(row=1, column=0)
password_obj.grid(row=3, column=0)

def login(form):
    forget_login_window()
    next_window(form)

def authenticate_user():
    environment_checker = None
    if sandbox.get():
        environment_checker = "SANDBOX"
    if production.get():
        environment_checker = "PRODUCTION"
    auth_obj = AuthenticationAPI(None, constants.v2_api.get(environment_checker))
    response = auth_obj.login(username.get(), password.get())
    access_token = json.loads(response).get("auth_token")
    if access_token:
        return True
    return False

def check_login():
    environment = [sandbox.get(), production.get()]
    try:
        if not username.get() and not password.get():
            if any(environment):
                no_env.grid_forget()
            bad_pass.grid(row=4, column=0, sticky=constants.WIDGET_REGION)

        if not any(environment) and not environment[0] and not environment[1]:
            no_env.grid(row=8, column=0, sticky=constants.WIDGET_REGION)
        
        if environment[0] and environment[1]:
            no_env.grid(row=8, column=0, sticky=constants.WIDGET_REGION)
        else:
            re = authenticate_user()
            if re:
                if not any(environment) and not environment[0] and not environment[1]:
                    no_env.grid(row=8, column=0, sticky=constants.WIDGET_REGION)
                    bad_pass.grid_forget()
                elif environment[0] and environment[1]:
                    no_env.grid(row=8, column=0, sticky=constants.WIDGET_REGION)
                else:
                    login('Reports Page')
                    # bad_pass.grid(row=4, column=0, sticky=constants.WIDGET_REGION)
            else:
                if any(environment):
                    no_env.grid_forget()
                bad_pass.grid(row=4, column=0, sticky=constants.WIDGET_REGION)
    except Exception as err:
        bad_pass.grid(row=4, column=0, sticky=constants.WIDGET_REGION)
        log.error(str(err))


loginButton = Button(root, text="Login", width=18, bg="white", highlightbackground="#98fb98", font=constants.WIDGET_FONT_COLOR, command=check_login)
cancelButton = Button(root, text="Cancel", width=15, bg="white", highlightbackground="red", font=constants.WIDGET_FONT_COLOR, command=quit)
loginButton.grid(row=9, column=0)
cancelButton.grid(row=10, column=0)

# New window

def forget_login_window():
    username_obj.grid_forget()
    password_obj.grid_forget()
    user_label.grid_forget()
    pass_label.grid_forget()
    loginButton.grid_forget()
    cancelButton.grid_forget()
    bad_pass.grid_forget()
    no_env.grid_forget()
    env_label.grid_forget()
    check_sand.grid_forget()
    check_prod.grid_forget()
    # root.geometry("600x500")

    # root.geometry(600*600)


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
mismatch = IntVar()
uncollected = IntVar()
user_ranking = IntVar()
company_user = IntVar()

scheduled_report = IntVar()
custom_report = IntVar()

report_type = None

start_date = StringVar()
end_date = StringVar()

input_time = StringVar()
time_entered = None
period_format_am = StringVar()
period_format_pm = StringVar()
period_format = None

report_path = ""

def database():
    conn = sqlite3.connect('database.db')
    connection = conn.cursor()
    connection.execute("CREATE TABLE IF NOT EXISTS powertbl(id integer primary key autoincrement, name TEXT, password TEXT, api_key TEXT, start_date TEXT, end_date TEXT, reports TEXT, report_path TEXT, created_at DATETIME NOT NULL, report_type TEXT, environment TEXT)")
    conn.commit()

database()

report_label_error = Label(root, text="please select one report type", foreground="red")

report_start_label = Label(root, text= "Report start date", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR)
report_start_date = DateEntry(root, locale='en_US', date_pattern='y-mm-dd', width= 16, background= constants.FOREGOUND_COLOR_BLUE, textvariable=start_date, foreground= constants.FOREGOUND_COLOR_DARK, bd=2)
report_end_label = Label(root, text= "Report end date", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR)
report_end_date = DateEntry(root,locale='en_US', date_pattern='y-mm-dd', width= 16, background= constants.FOREGOUND_COLOR_BLUE, textvariable=end_date,  foreground= constants.FOREGOUND_COLOR_DARK, bd=2)

schedule_label = Label(root, text = "Enter schedule time for report. Default time is 10:00 A.M")
input_entry = Entry(root, textvariable=input_time, width=8)
time_format_label = Label(root, foreground="red", text="Note: Please enter time in format like 11:15 or 4:10..")
time_format_am = Checkbutton(root, text = "A.M", variable=period_format_am, font=constants.WIDGET_FONT_COLOR)
time_format_pm = Checkbutton(root, text = "P.M", variable=period_format_pm, font=constants.WIDGET_FONT_COLOR)

def show_custom_schedule_format():
    if custom_report.get() and scheduled_report.get():
        schedule_label.grid_forget()
        # input_entry.insert(0, "")
        input_entry.grid_forget()
        time_format_label.grid_forget()
        time_format_am.grid_forget()
        time_format_pm.grid_forget()
        report_start_label.grid_forget()
        report_start_date.grid_forget()
        report_end_label.grid_forget()
        report_end_date.grid_forget()
        # report_label_error.grid(row=14, column=0, sticky=constants.WIDGET_REGION)
    elif not custom_report.get() and not scheduled_report.get():
        schedule_label.grid_forget()
        # input_entry.insert(0, "")
        input_entry.grid_forget()
        time_format_label.grid_forget()
        time_format_am.grid_forget()
        time_format_pm.grid_forget()
        report_start_label.grid_forget()
        report_start_date.grid_forget()
        report_end_label.grid_forget()
        report_end_date.grid_forget()
    elif custom_report.get():
        schedule_label.grid_forget()
        # input_entry.insert(0, "")
        input_entry.grid_forget()
        time_format_label.grid_forget()
        time_format_am.grid_forget()
        time_format_pm.grid_forget()
        # report_label_error.grid_forget()

        report_start_label.grid(row=14, sticky=constants.WIDGET_REGION)
        report_start_date.grid(row=15, sticky="w")
        report_end_label.grid(row=16, sticky=constants.WIDGET_REGION)
        report_end_date.grid(row=17, sticky="w")
    elif scheduled_report.get():
        report_start_label.grid_forget()
        report_start_date.grid_forget()
        report_end_label.grid_forget()
        report_end_date.grid_forget()
        # report_label_error.grid_forget()

        schedule_label.grid(row=14, sticky=constants.WIDGET_REGION)
        input_entry.grid(row=15, sticky=constants.WIDGET_REGION)
        input_entry.delete(0, END)
        input_entry.insert(0, "10:00")
        time_format_label.grid(row=16, sticky=constants.WIDGET_REGION)
        time_format_am.grid(row=17, column=0, sticky=constants.WIDGET_REGION)
        time_format_pm.grid(row=17, column=1, sticky=constants.WIDGET_REGION)

        # Label(root, text= "Report start date",fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=11, sticky=constants.WIDGET_REGION)
        # DateEntry(root,locale='en_US', date_pattern='y-mm-dd', width= 16, state='disabled', background= constants.FOREGOUND_COLOR_BLUE, textvariable=start_date, foreground= constants.FOREGOUND_COLOR_DARK, bd=2).grid(row=12, sticky="w")
        # Label(root, text= "Report end date", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=13, sticky=constants.WIDGET_REGION)
        # DateEntry(root, locale='en_US', date_pattern='y-mm-dd', state='disabled', width= 16, background= constants.FOREGOUND_COLOR_BLUE, textvariable=end_date,  foreground= constants.FOREGOUND_COLOR_DARK, bd=2).grid(row=14, sticky="w")

def get_start_date():
    return start_date.get()


def get_end_date():
    return end_date.get()


def open_dialog():
    global report_path
    report_path =  filedialog.askdirectory(initialdir='/', title='select the location for report to be downloaded')
    Label(root, text=f"reports will reside in directory: {report_path}", foreground="red", font=constants.WIDGET_FONT_COLOR).grid(row=21, sticky=constants.WIDGET_REGION)

def delete(window):
    global error_window
    window.destroy()
    error_window = False

def delete_sch(roo):
    roo.destroy()

period_format_am = IntVar()
period_format_pm = IntVar()

def schedule_success():
    global time_entered, period_format
    reports_check = [survey_results.get(), reviews_management.get(), survey_statistics.get(), publish_history.get(), hierarchy_details.get(), verified_users.get(), nps_trend.get(), account_statistics.get(),
                    sms_delivery.get(), survey_email.get(), nps.get(), ranking_tier.get(), incomplete_survey.get(), mismatch.get(), company_user.get(),
                    user_ranking.get(), uncollected.get()]
    report_occurance = reports_check.count(1)
    if report_occurance > 1:
        msgbox.showinfo(title='success!', message=f"Requested reports are scheduled to run daily at {time_entered}{period_format}")
    else:
        msgbox.showinfo(title='success!', message=f"Requested report is scheduled to run daily at {time_entered}{period_format}")
    root.destroy()


def custom_success():
    reports_check = [survey_results.get(), reviews_management.get(), survey_statistics.get(), publish_history.get(), hierarchy_details.get(), verified_users.get(), nps_trend.get(), account_statistics.get(),
                    sms_delivery.get(), survey_email.get(), nps.get(), ranking_tier.get(), incomplete_survey.get(), mismatch.get(), company_user.get(),
                    user_ranking.get(), uncollected.get()]
    report_occurance = reports_check.count(1)
    if report_occurance > 1:
        msgbox.showinfo(title='success!', message='Thank You, requested reports will be generated')
    else:
        msgbox.showinfo(title='success!', message='Thank You, requested report will be generated')   
    root.destroy()

def report_generation(obj):
    obj.generate_data()


def error_window_screen(dimension, text_field):
    global error_window
    error_window = True
    error_window = Toplevel(root)
    error_window.attributes('-topmost', 'true')
    error_window.geometry(dimension)
    error_window.resizable(False, False)
    error_window.title("Warning!")
    Label(error_window, text=text_field, fg="red").grid(row=0)
    Button(error_window, text="OK", command= lambda: delete(error_window)).grid(row=1)


error_win_label_report = Label(root, text="please select a report", foreground="red")
error_win_report_type = Label(root, text="please select a report type", foreground="red")
error_win_report_path = Label(root, text="please select report path", foreground="red")

def register_user():
    """after successfull verification saving the user"""
    global error_window, username, password, survey_results, reviews_management, survey_statistics, publish_history, hierarchy_details, report_path
    global verified_users, nps_trend, account_statistics, sms_delivery, survey_email, nps, ranking_tier, incomplete_survey, sandbox, production
    global scheduled_report, custom_report, report_type, mismatch, company_user, user_ranking, uncollected
    # report_type = ""

    reports_check = [survey_results.get(), reviews_management.get(), survey_statistics.get(), publish_history.get(), hierarchy_details.get(), verified_users.get(), nps_trend.get(), account_statistics.get(),
                    sms_delivery.get(), survey_email.get(), nps.get(), ranking_tier.get(), incomplete_survey.get(), mismatch.get(), company_user.get(),
                    user_ranking.get(), uncollected.get()]
    

    report_type = [scheduled_report.get(), custom_report.get()]

    if not any(reports_check):
        if not report_path:
            error_win_report_path.grid(row=20, sticky=constants.WIDGET_REGION)
        else:
            error_win_report_path.grid_forget()
        if not any(report_type):
            error_win_report_type.grid(row=18, sticky=constants.WIDGET_REGION)
        else:
            error_win_report_type.grid_forget()
        error_win_label_report.grid(row=11, sticky=constants.WIDGET_REGION)
    if not report_path:
        if not any(reports_check):
            error_win_label_report.grid(row=11, sticky=constants.WIDGET_REGION)
        else:
            error_win_label_report.grid_forget()
        if not any(report_type):
            error_win_report_type.grid(row=18, sticky=constants.WIDGET_REGION)
        else:
            error_win_report_type.grid_forget()
        error_win_report_path.grid(row=20, sticky=constants.WIDGET_REGION)
    if not any(report_type):
        if not any(reports_check):
            error_win_label_report.grid(row=11, sticky=constants.WIDGET_REGION)
        else:
            error_win_label_report.grid_forget()
        if not report_path:
            error_win_report_path.grid(row=20, sticky=constants.WIDGET_REGION)
        else:
            error_win_report_path.grid_forget()
        error_win_report_type.grid(row=18, sticky=constants.WIDGET_REGION)
    # if scheduled_report.get():
    #     report_type = "scheduler"
    # else:
    #     report_type = "custom"
    if any(reports_check) and report_path and any(report_type):
        error_win_report_type.grid_forget()
        error_win_report_path.grid_forget()
        error_win_label_report.grid_forget()
        if report_type[0] and report_type[1]:
            report_label_error.grid(row=11, sticky=constants.WIDGET_REGION)
        else:
            report_label_error.grid_forget()
            report_type_format = None
            if scheduled_report.get():
                report_type_format = "scheduler"
            else:
                report_type_format = "custom"
            print('correct')
            ingest_data(report_type_format)

def ingest_data(report_type):
    """adding user details to the database"""
    global report_path, input_time, period_format_am, period_format_pm, period_format, time_entered
    total_reports = {}
    environment = {}

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
    if mismatch.get():
        total_reports["mismatch_transactions_report"] = "mismatch"
    if uncollected.get():
        total_reports["uncollected_transactions_report"] = "uncollected"
    if user_ranking.get():
        total_reports["user_ranking_report"] = "userranking"
    if company_user.get():
        total_reports["company_user_report"] = "companyuser"
    
    if sandbox.get():
        environment =  "SANDBOX"
    if production.get():
        environment = "PRODUCTION"
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
            try:
                reports_data = (None, username.get(), str(encryped_password, 'UTF-8'), str(decrypt_key, 'UTF-8'), start_date, end_date, total_reports, report_path, created_at, report_type, environment)
                log.info(f'custom report is selected by user {username}, {str(decrypt_key)} and requested data is {reports_data}')
                # success()
                powerbi_ingestion = PowerBIDataIngestion(constants.v2_api.get('PREPROD'), constants.report_api.get('PREPROD'), reports_data)
                # thread = threading.Thread(target=report_generation, args=(powerbi_ingestion, ))
                # thread.start()
                custom_success()
                powerbi_ingestion.generate_data()
            except Exception as err:
                log.error(f'custom report selection failed for user {username.get()}, {str(decrypt_key)}: {str(err)}')
            finally:
                log.info(f'reports data inserted for {username.get()}, {str(decrypt_key)}')
                connection.execute('INSERT INTO powertbl(name, password, api_key, start_date, end_date, reports, report_path, created_at, report_type, environment) VALUES(?,?,?,?,?,?,?,?,?,?)', (username.get(), encryped_password, decrypt_key, start_date, end_date, json.dumps(total_reports), report_path, created_at, report_type, environment))
                conn.commit()
        else:
            time_entered = input_time.get() if input_time.get() else "10:00"
            print(time_entered)
            period_format = None
            format_entered = [period_format_am.get(), period_format_pm.get()]
            if any(format_entered):
                if format_entered[0] and format_entered[1]:
                    period_format = "am"
                else:
                    if format_entered[0]:
                        period_format = "am"
                    else:
                        period_format = "pm"
            else:
                period_format = 'am'
            log.info(f'Scheduled report is selected by user {username.get()}, {str(decrypt_key)}')
            connection.execute('INSERT INTO powertbl(name, password, api_key, start_date, end_date, reports, report_path, created_at, report_type, environment) VALUES(?,?,?,?,?,?,?,?,?,?)', (username.get(), encryped_password, decrypt_key, start_date, end_date, json.dumps(total_reports), report_path, created_at, report_type, environment))
            conn.commit()
            scheduled_time = time_entered + period_format
            task_name = "Task"+random.randint(1,10000)
            task_schedule = subprocess.Popen(['powershell.exe','-ExecutionPolicy', 'Unrestricted', constants.PS1_SCRIPT_PATH, scheduled_time, task_name], stdout=sys.stdout)
            task_schedule.communicate()
            schedule_success()
    except Exception as err:
        log.error(f"issue occured for user {username.get()}, {str(decrypt_key)}: {str(err)}")
        log.exception(err)

def next_window(obj):
    root.title(obj)

    Label(root, text= "Select report/reports *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=1, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Survey Results", variable=survey_results, font=constants.WIDGET_FONT_COLOR).grid(row=2, column=0, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Reviews_Management", variable=reviews_management, font=constants.WIDGET_FONT_COLOR).grid(row=2, column=1, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Publish History", variable=publish_history, font=constants.WIDGET_FONT_COLOR).grid(row=3, column=0, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Hierarchy Details", variable=hierarchy_details, font=constants.WIDGET_FONT_COLOR).grid(row=3, column=1, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "NPS Trend", variable=nps_trend, font=constants.WIDGET_FONT_COLOR).grid(row=4, column=0, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Account Statistics", variable=account_statistics, font=constants.WIDGET_FONT_COLOR).grid(row=4, column=1, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "SMS Delivery", variable=sms_delivery, font=constants.WIDGET_FONT_COLOR).grid(row=5, column=0, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Survey Email", variable=survey_email, font=constants.WIDGET_FONT_COLOR).grid(row=5, column=1, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Verified Users", variable=verified_users, font=constants.WIDGET_FONT_COLOR).grid(row=6, column=0, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "NPS", variable=nps, font=constants.WIDGET_FONT_COLOR).grid(row=6, column=1, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Ranking Tier", variable=ranking_tier, font=constants.WIDGET_FONT_COLOR).grid(row=7, column=0, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Incomplete Survey", variable=incomplete_survey, font=constants.WIDGET_FONT_COLOR).grid(row=7, column=1, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Survey Statistics", variable=survey_statistics, font=constants.WIDGET_FONT_COLOR).grid(row=8, column=0, sticky=constants.WIDGET_REGION)

    Checkbutton(root, text = "Mismatch", variable=mismatch, font=constants.WIDGET_FONT_COLOR).grid(row=8, column=1,sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Uncollected", variable=uncollected, font=constants.WIDGET_FONT_COLOR).grid(row=9, column=0, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "User Ranking", variable=user_ranking, font=constants.WIDGET_FONT_COLOR).grid(row=9, column=1, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Company User", variable=company_user, font=constants.WIDGET_FONT_COLOR).grid(row=10, column=0, sticky=constants.WIDGET_REGION)

    Label(root, text= "Select report type *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=12, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Schedule", variable=scheduled_report, font=constants.WIDGET_FONT_COLOR, command=show_custom_schedule_format).grid(row=13, column=0, sticky=constants.WIDGET_REGION)
    Checkbutton(root, text = "Custom", variable=custom_report, font=constants.WIDGET_FONT_COLOR, command=show_custom_schedule_format).grid(row=13,column=1, sticky=constants.WIDGET_REGION)

    Button(root, text="Choose report path", width=20, font=constants.WIDGET_FONT_COLOR, command=open_dialog).grid(row=19, sticky=constants.WIDGET_REGION)
    Button(root, text="Submit", width="18", bg="white", highlightbackground="#98fb98", command=register_user, font=constants.WIDGET_FONT_COLOR).grid(row=22, sticky=constants.WIDGET_REGION)



root.mainloop()