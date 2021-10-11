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
  
tabControl.add(tab1, text ='User details')
tabControl.add(tab2, text ='Report details')
tabControl.pack(fill='both', expand=1)
  
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
report_path = "/"

def database():
    conn = sqlite3.connect('database.db')
    connection = conn.cursor()
    connection.execute("CREATE TABLE IF NOT EXISTS powertbl(id integer primary key autoincrement, name TEXT, password TEXT, start_date TEXT, end_date TEXT, reports TEXT, environment TEXT, report_path TEXT, created_at DATETIME NOT NULL)")
    conn.commit()

database()


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
    report_path =  filedialog.askdirectory(initialdir='/', title='select the location for report to be downloaded')
    Label(tab2, text=f"reports will reside in directory: {report_path}", foreground="red", font=("times new roman", 15)).grid(row=18, sticky='w')


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
            error_window_screen_username_password("280x100", "username and password fields are required.")
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
        connection.execute('INSERT INTO powertbl(name, password, start_date, end_date, reports, environment, report_path, created_at) VALUES(?,?,?,?,?,?,?,?)', (username.get(), encryped_password, start_date, end_date, json.dumps(total_reports), environment, report_path, decrypt_key, created_at))
        conn.commit()
        success()
    except Exception as err:
        print(str(err))

# design layout
Label(tab1, text="Username *", fg="DodgerBlue", font=("times new roman", 15, "bold")).grid(row=0, sticky='w')
Entry(tab1, textvariable=username, bg="lightgray", width=25).grid(row=1, sticky='w')
Label(tab1, text= "Password *", fg='DodgerBlue', font=("times new roman", 15, "bold")).grid(row=3, sticky='w')
Entry(tab1, textvariable=password, bg="lightgray", width=25, show="*").grid(row=4, sticky='w')
Button(tab1, text='Switch to reports', command=select_tab, font=("times new roman", 15, "bold")).grid(row=5, sticky='w')

Label(tab2, text= "Select report/reports *", fg='DodgerBlue', font=("times new roman", 15, "bold")).grid(row=1, sticky='w')
Checkbutton(tab2, text = "Survey Results", variable=survey_results, font=("times new roman", 15, "bold")).grid(row=2, column=0, sticky='w')
Checkbutton(tab2, text = "Reviews_Management", variable=reviews_management, font=("times new roman", 15, "bold")).grid(row=2, column=1, sticky='w')
Checkbutton(tab2, text = "Publish History", variable=publish_history, font=("times new roman", 15, "bold")).grid(row=3, column=0, sticky='w')
Checkbutton(tab2, text = "Hierarchy Details", variable=hierarchy_details, font=("times new roman", 15, "bold")).grid(row=3, column=1, sticky='w')
Checkbutton(tab2, text = "NPS Trend", variable=nps_trend, font=("times new roman", 15, "bold")).grid(row=4, column=0, sticky='w')
Checkbutton(tab2, text = "Account Statistics", variable=account_statistics, font=("times new roman", 15, "bold")).grid(row=4, column=1, sticky='w')
Checkbutton(tab2, text = "SMS Delivery", variable=sms_delivery, font=("times new roman", 15, "bold")).grid(row=5, column=0, sticky='w')
Checkbutton(tab2, text = "Survey Email", variable=survey_email, font=("times new roman", 15, "bold")).grid(row=5, column=1, sticky='w')
Checkbutton(tab2, text = "Verified Users", variable=verified_users, font=("times new roman", 15, "bold")).grid(row=6, column=0, sticky='w')
Checkbutton(tab2, text = "NPS", variable=nps, font=("times new roman", 15, "bold")).grid(row=6, column=1, sticky='w')
Checkbutton(tab2, text = "Ranking Tier", variable=ranking_tier, font=("times new roman", 15, "bold")).grid(row=7, column=0, sticky='w')
Checkbutton(tab2, text = "Incomplete Survey", variable=incomplete_survey, font=("times new roman", 15, "bold")).grid(row=7, column=1, sticky='w')
Checkbutton(tab2, text = "Survey Statistics", variable=survey_statistics, font=("times new roman", 15, "bold")).grid(row=8, sticky='w')
Label(tab2, text= "Report start date", fg='DodgerBlue', font=("times new roman", 15, "bold")).grid(row=9, sticky='w')
DateEntry(tab2, width= 16, background= "DodgerBlue3", textvariable=start_date, foreground= "darkblue", bd=2).grid(row=10, sticky="w")
Label(tab2, text= "Report end date", fg='DodgerBlue', font=("times new roman", 15, "bold")).grid(row=11, sticky='w')
DateEntry(tab2, width= 16, background= "DodgerBlue3", textvariable=end_date,  foreground= "darkblue", bd=2).grid(row=12, sticky="w")
# Label(tab2, foreground="red", text="Note: If start and end dates are not selected, present date will be taken.").grid(row=13, sticky='w')

Label(tab2, text="Select environment *", fg='DodgerBlue', font=("times new roman", 15, "bold")).grid(row=14, sticky='w')
Checkbutton(tab2, text = "Sandbox", variable=sandbox, font=("times new roman", 15, "bold")).grid(row=15, sticky='w')
Checkbutton(tab2, text = "Production", variable=production, font=("times new roman", 15, "bold")).grid(row=15, column=1, sticky='w')
Button(tab2, text="Select path", width=20, font=("times new roman", 15, "bold"), command=open_dialog).grid(row=17, sticky='w')
Button(tab2, text="Submit", width="18", bg="white", highlightbackground="#98fb98", command=register_user, font=("times new roman", 15, "bold")).grid(row=20, sticky='w')
  
root.mainloop()
