TK_SILENCE_DEPRECATION=1
import tkinter as tk
from tkinter import *
from tkcalendar import *
import sqlite3
import hashlib, binascii, os
import re
import tkinter.messagebox as msgbox
import json

from tkcalendar import dateentry
from datetime import datetime


root = tk.Tk()
root.geometry("700x600")
root.resizable(False, False)
root.title("Experience.com reports form")
error_window = False
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
    connection.execute("CREATE TABLE IF NOT EXISTS powertbl(id integer primary key autoincrement, name TEXT, password TEXT, start_date TEXT, end_date TEXT, reports TEXT, environment TEXT, created_at DATETIME NOT NULL)")
    conn.commit()

database()

def delete(window):
    global error_window
    window.destroy()
    error_window = False


def success():
    msgbox.showinfo(title='success!', message='Thank You, requested report will be generated')
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

def get_start_date():
    return start_date.get()

def get_end_date():
    return end_date.get()

def password_hash(password):
    """hashing the password"""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def register_user():
    """after successfull verification saving the user"""
    global error_window, username, password, survey_results, reviews_management, survey_statistics, publish_history, hierarchy_details
    global verified_users, nps_trend, account_statistics, sms_delivery, survey_email, nps, ranking_tier, incomplete_survey, sandbox, production
    username_text = username.get()
    password_text = password.get()

    reports_check = [survey_results.get(), reviews_management.get(), survey_statistics.get(), publish_history.get(), hierarchy_details.get(), verified_users.get(), nps_trend.get(), account_statistics.get(),
                    sms_delivery.get(), survey_email.get(), nps.get(), ranking_tier.get(), incomplete_survey.get()]
    
    environment_check = [sandbox.get(), production.get()]
    
    # user_exists = None

    if not username_text or not password_text:
        if not error_window:
            # width and height for err win
            error_window_screen("280x100", "username and password fields are required.")
    elif not any(reports_check):
        if not error_window:
            error_window_screen("220x100", "please select a report.")
    elif not any(environment_check):
        if not error_window:
            error_window_screen("280x100", "please select a environment to get report.")  
    else:
        hashed_password = password_hash(password_text)
        save_data(hashed_password)



def save_data(hashed_password):
    """adding user details to the database"""
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
        environment['sandbox'] = "sandbox_reports"
    if production.get():
        environment['production'] = "production_reports"
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

        connection.execute('INSERT INTO powertbl(name, password, start_date, end_date, reports, environment, created_at) VALUES(?,?,?,?,?,?,?)', (username.get(), hashed_password, start_date, end_date, json.dumps(total_reports), json.dumps(environment), created_at))
        conn.commit()
        success()
    except Exception as err:
        print(str(err))

Label(root, text="Username *", fg="magenta", font=("times new roman", 15, "bold")).grid(row=0, sticky='w')
Entry(root, textvariable=username, bg="lightgray", width=25).grid(row=1, sticky='w')
Label(root, text= "Password *", fg='magenta', font=("times new roman", 15, "bold")).grid(row=3, sticky='w')
Entry(root, textvariable=password, bg="lightgray", width=25, show="*").grid(row=4, sticky='w')

Label(root, text= "Select report/reports *", fg='magenta', font=("times new roman", 15, "bold")).grid(row=5, sticky='w')
Checkbutton(root, text = "Survey Results", variable=survey_results, font=("times new roman", 15, "bold")).grid(row=6, column=0, sticky='w')
Checkbutton(root, text = "Reviews_Management", variable=reviews_management, font=("times new roman", 15, "bold")).grid(row=6, column=1, sticky='w')
Checkbutton(root, text = "Publish History", variable=publish_history, font=("times new roman", 15, "bold")).grid(row=7, column=0, sticky='w')
Checkbutton(root, text = "Hierarchy Details", variable=hierarchy_details, font=("times new roman", 15, "bold")).grid(row=7, column=1, sticky='w')
Checkbutton(root, text = "NPS Trend", variable=nps_trend, font=("times new roman", 15, "bold")).grid(row=8, column=0, sticky='w')
Checkbutton(root, text = "Account Statistics", variable=account_statistics, font=("times new roman", 15, "bold")).grid(row=8, column=1, sticky='w')
Checkbutton(root, text = "SMS Delivery", variable=sms_delivery, font=("times new roman", 15, "bold")).grid(row=9, column=0, sticky='w')
Checkbutton(root, text = "Survey Email", variable=survey_email, font=("times new roman", 15, "bold")).grid(row=9, column=1, sticky='w')
Checkbutton(root, text = "Verified Users", variable=verified_users, font=("times new roman", 15, "bold")).grid(row=10, column=0, sticky='w')
Checkbutton(root, text = "NPS", variable=nps, font=("times new roman", 15, "bold")).grid(row=10, column=1, sticky='w')
Checkbutton(root, text = "Ranking Tier", variable=ranking_tier, font=("times new roman", 15, "bold")).grid(row=11, column=0, sticky='w')
Checkbutton(root, text = "Incomplete Survey", variable=incomplete_survey, font=("times new roman", 15, "bold")).grid(row=11, column=1, sticky='w')
Checkbutton(root, text = "Survey Statistics", variable=survey_statistics, font=("times new roman", 15, "bold")).grid(row=12, sticky='w')
Label(root, text= "Report start date", fg='magenta', font=("times new roman", 15, "bold")).grid(row=13, sticky='w')
DateEntry(root, width= 16, background= "magenta3", textvariable=start_date, foreground= "white",bd=2).grid(row=14, sticky="w")
Label(root, text= "Report end date", fg='magenta', font=("times new roman", 15, "bold")).grid(row=15, sticky='w')
DateEntry(root, width= 16, background= "magenta3", textvariable=end_date,  foreground= "white",bd=2).grid(row=16, sticky="w")
Label(root, foreground="red", text="Note: If start and end dates are not selected, present date will be taken.").grid(row=17, sticky='w')

Label(root, text="Choose environment *", fg='magenta', font=("times new roman", 15, "bold")).grid(row=18, sticky='w')
Checkbutton(root, text = "Sandbox", variable=sandbox, font=("times new roman", 15, "bold")).grid(row=19, sticky='w')
Checkbutton(root, text = "Production", variable=production, font=("times new roman", 15, "bold")).grid(row=20, sticky='w')


Button(root, text="Submit", width="18", bg="white", highlightbackground="#98fb98", command=register_user, font=("times new roman", 15, "bold")).grid(row=22, sticky='w')

root.mainloop()