TK_SILENCE_DEPRECATION=1
import tkinter as tk
from tkinter import *
from tkcalendar import *
from tkinter import ttk
import sqlite3
import tkinter.messagebox as msgbox
from tkinter import filedialog
import json
from powerbi.power_bi_integration import PowerBIDataIngestion
from powerbi import crypto
from powerbi import constants
from tkcalendar import dateentry
from datetime import datetime
from cryptography.fernet import Fernet


# tkinter obj configs
root = tk.Tk()
root.geometry("600x600")
root.resizable(False, False)
# root.geometry("700x500")
root.title("Experience.com reports form")

# variables for reports
error_window = False

report_path = "/"

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

def database():
    conn = sqlite3.connect('database.db')
    connection = conn.cursor()
    connection.execute("CREATE TABLE IF NOT EXISTS powertbl(id integer primary key autoincrement, name TEXT, password TEXT, start_date TEXT, end_date TEXT, reports TEXT, environment TEXT, report_path TEXT, api_key BLOB, created_at DATETIME NOT NULL)")
    conn.commit()

database()


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


def open_dialog():
    global report_path
    report_path =  filedialog.askdirectory(initialdir='/', title='select the location for report to be downloaded')
    Label(root, text=f"reports will reside in directory: {report_path}", foreground="red", font=constants.WIDGET_FONT_COLOR).grid(row=22, sticky=constants.WIDGET_REGION)


def get_start_date():
    return start_date.get()


def get_end_date():
    return end_date.get()


def register_user():
    """after successfull verification saving the user"""
    global error_window, username, password, survey_results, reviews_management, survey_statistics, publish_history, hierarchy_details
    global verified_users, nps_trend, account_statistics, sms_delivery, survey_email, nps, ranking_tier, incomplete_survey, sandbox, production
    username_text = username.get()
    password_text = password.get()

    reports_check = [survey_results.get(), reviews_management.get(), survey_statistics.get(), publish_history.get(), hierarchy_details.get(), verified_users.get(), nps_trend.get(), account_statistics.get(),
                    sms_delivery.get(), survey_email.get(), nps.get(), ranking_tier.get(), incomplete_survey.get()]
    
    environment_check = [sandbox.get(), production.get()]

    if not username_text or not password_text:
        if not error_window:
            # width and height for err win
            error_window_screen("280x100", "username and password fields are required.")
    elif not any(reports_check):
        if not error_window:
            error_window_screen("220x100", "please select a report.")
    elif not any(environment_check):
        if not error_window:
            error_window_screen("300x100", "please select a environment to generate report.")  
    else:
        ingest_data()


def ingest_data():
    """adding user details to the database"""
    global report_path
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
        reports_data = (None, username.get(), str(encryped_password, 'UTF-8'), str(decrypt_key, 'UTF-8'), start_date, end_date, total_reports, report_path)
        # powerbi_ingestion = PowerBIDataIngestion(constants.v2_api.get(environment), constants.report_api.get(environment), reports_data)
        # powerbi_ingestion.generate_data()
        connection.execute('INSERT INTO powertbl(name, password, start_date, end_date, reports, environment, report_path, api_key, created_at) VALUES(?,?,?,?,?,?,?,?,?)', (username.get(), encryped_password, start_date, end_date, json.dumps(total_reports), environment, report_path, decrypt_key, created_at))
        conn.commit()
        success()
    except Exception as err:
        print(str(err))

# layout design
Label(root, text="Username *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=0, sticky=constants.WIDGET_REGION)
Entry(root, textvariable=username, bg="lightgray", width=25).grid(row=1, sticky=constants.WIDGET_REGION)
Label(root, text= "Password *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=3, sticky=constants.WIDGET_REGION)
Entry(root, textvariable=password, bg="lightgray", width=25, show="*").grid(row=4, sticky=constants.WIDGET_REGION)


Label(root, text= "Select report/reports *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=5, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Survey Results", variable=survey_results, font=constants.WIDGET_FONT_COLOR).grid(row=6, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Reviews_Management", variable=reviews_management, font=constants.WIDGET_FONT_COLOR).grid(row=6, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Publish History", variable=publish_history, font=constants.WIDGET_FONT_COLOR).grid(row=7, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Hierarchy Details", variable=hierarchy_details, font=constants.WIDGET_FONT_COLOR).grid(row=7, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "NPS Trend", variable=nps_trend, font=constants.WIDGET_FONT_COLOR).grid(row=8, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Account Statistics", variable=account_statistics, font=constants.WIDGET_FONT_COLOR).grid(row=8, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "SMS Delivery", variable=sms_delivery, font=constants.WIDGET_FONT_COLOR).grid(row=9, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Survey Email", variable=survey_email, font=constants.WIDGET_FONT_COLOR).grid(row=9, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Verified Users", variable=verified_users, font=constants.WIDGET_FONT_COLOR).grid(row=10, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "NPS", variable=nps, font=constants.WIDGET_FONT_COLOR).grid(row=10, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Ranking Tier", variable=ranking_tier, font=constants.WIDGET_FONT_COLOR).grid(row=11, column=0, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Incomplete Survey", variable=incomplete_survey, font=constants.WIDGET_FONT_COLOR).grid(row=11, column=1, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Survey Statistics", variable=survey_statistics, font=constants.WIDGET_FONT_COLOR).grid(row=12, sticky=constants.WIDGET_REGION)
Label(root, text= "Report start date", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=13, sticky=constants.WIDGET_REGION)
DateEntry(root, width= 16, background= constants.FOREGOUND_COLOR_BLUE, textvariable=start_date, foreground= constants.FOREGOUND_COLOR_DARK, bd=2).grid(row=14, sticky="w")
Label(root, text= "Report end date", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=15, sticky=constants.WIDGET_REGION)
DateEntry(root, width= 16, background= constants.FOREGOUND_COLOR_BLUE, textvariable=end_date,  foreground= constants.FOREGOUND_COLOR_DARK, bd=2).grid(row=16, sticky="w")
# Label(root, foreground="red", text="Note: If start and end dates are not selected, present date will be taken.").grid(row=17, sticky=constants.WIDGET_REGION)

Label(root, text="Select environment *", fg=constants.FOREGOUND_COLOR_BLUE, font=constants.WIDGET_FONT_COLOR).grid(row=18, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Sandbox", variable=sandbox, font=constants.WIDGET_FONT_COLOR).grid(row=19, sticky=constants.WIDGET_REGION)
Checkbutton(root, text = "Production", variable=production, font=constants.WIDGET_FONT_COLOR).grid(row=19, column=1, sticky=constants.WIDGET_REGION)
Button(root, text="Select path", width=20, font=constants.WIDGET_FONT_COLOR, command=open_dialog).grid(row=21, sticky=constants.WIDGET_REGION)


Button(root, text="Submit", width="18", bg="white", highlightbackground="#98fb98", command=register_user, font=constants.WIDGET_FONT_COLOR).grid(row=24, sticky=constants.WIDGET_REGION)

root.mainloop()