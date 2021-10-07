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


screen = tk.Tk()
screen.geometry("700x700")
screen.resizable(False, False)
screen.title("Experience.com reports form")
error_window = False
start_date = None
end_date = None

def database():
    conn = sqlite3.connect('database.db')
    connection = conn.cursor()
    connection.execute("CREATE TABLE IF NOT EXISTS powertbl(id integer primary key autoincrement, name TEXT, password TEXT, start_date TEXT, end_date TEXT, reports TEXT, environment TEXT, created_at DATETIME NOT NULL)")
    conn.commit()

database()

def error_window_screen(dimension, text_field):
    global error_window
    error_window = True
    error_window = Toplevel(screen)
    error_window.attributes('-topmost', 'true')
    error_window.geometry(dimension)
    error_window.title("Warning!")
    Label(error_window, text=text_field, fg="red").pack()
    Button(error_window, text="OK", command= lambda: delete(error_window)).pack()

def password_hash(password):
    """hashing the password"""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def user_name_check():
    """check username already exists"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM powertbl WHERE name = ?", (username.get(), ))
    username_count = cursor.fetchone()[0]
    if username_count >= 1:
        print('username already exists, please select another name')
        return False
    return True


def delete(window):
    global error_window
    window.destroy()
    error_window = False


def success():
    msgbox.showinfo(title='success!', message='Thank You, registered successfully')
    screen.destroy()


def register_user():
    """after successfull verification saving the user"""
    global error_window, username, password, survey_results, reviews_management, survey_statistics, publish_history, hierarchy_details
    global verified_users, nps_trend, account_statistics, sms_delivery, survey_email, nps, ranking_tier, incomplete_survey, sandbox, production
    username_text = username.get()
    password_text = password.get()

    reports_check = [survey_results.get(), reviews_management.get(), survey_statistics.get(), publish_history.get(), hierarchy_details.get(), verified_users.get(), nps_trend.get(), account_statistics.get(),
                    sms_delivery.get(), survey_email.get(), nps.get(), ranking_tier.get(), incomplete_survey.get()]
    
    environemnt_check = [sandbox.get(), production.get()]
    
    # user_exists = None

    if not username_text or not password_text:
        if not error_window:
            # width and height for err win
            error_window_screen("280x100", "username and password fields are required.")
    elif not any(reports_check):
        if not error_window:
            error_window_screen("220x100", "please select a report.")
    elif not any(environemnt_check):
        if not error_window:
            error_window_screen("280x100", "please select a environment to get report.")  
    else:
        hashed_password = password_hash(password_text)
        save_data(hashed_password)


def save_data(hashed_password):
    """adding user details to the database"""
    global start_date
    global end_date
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
        current_date = datetime.strftime(utc_date_time, "%Y-%m-%d")
        created_at = datetime.strftime(utc_date_time, "%Y-%m-%d %H:%M:%S")
        start_date = start_date if start_date else current_date
        end_date = end_date if end_date else current_date
        connection.execute('INSERT INTO powertbl(name, password, start_date, end_date, reports, environment, created_at) VALUES(?,?,?,?,?,?,?)', (username.get(), hashed_password, start_date, end_date, json.dumps(total_reports), json.dumps(environment), created_at))
        conn.commit()
        success()
    except Exception as err:
        pass


def dateentry_view_start_date():
    def print_sel():
        global start_date
        start_date = cal.get_date()
        Label(text=start_date).place(x=120, y=502)
    top = tk.Toplevel(screen)

    # Label(top, text='Choose date').pack(padx=10, pady=10)
    cal = DateEntry(top, width=18, background='darkblue', foreground='white', borderwidth=5)
    cal.pack(padx=10, pady=10)
    # cal.bind(start_date, print_sel)
    Button(top, text="OK", command=lambda: [print_sel(), cal.destroy(), top.destroy()]).pack()

def dateentry_view_end_date():
    def print_sel():
        global end_date
        end_date = cal.get_date()
        Label(text= end_date).place(x=120, y=557)
    top = tk.Toplevel(screen)

    # Label(top, text='Choose date').pack(padx=10, pady=10)
    cal = DateEntry(top, width=18, background='darkblue', foreground='white', borderwidth=5)
    cal.pack(padx=10, pady=10)
    cal.bind(end_date, print_sel)
    Button(top, text="OK", command=lambda: [print_sel(), cal.destroy(), top.destroy()]).pack()


heading = Label(text="PowerBI report generation form", fg="black", bg="light blue", width="500", height="3", font=("times new roman", 15, "bold")).pack()

Label(text= "Username *", fg='magenta', font=("times new roman", 15, "bold")).place(x=15, y=70)
Label(text= "Password *", fg='magenta', font=("times new roman", 15, "bold")).place(x=17, y=125)

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

Entry(screen, textvariable=username, bg="lightgray", font=("times new roman", 15, "bold")).place(x=15, y=95, width=240)
Entry(screen, textvariable=password, show="*", bg="lightgray", font=("times new roman", 15, "bold")).place(x=15, y=145, width=240)


# checkboxes
Label(text= "Choose Report/Reports *", fg='magenta', font=("times new roman", 15, "bold")).place(x=15, y=180)
Checkbutton(screen, text = "Survey Results", variable=survey_results, font=("times new roman", 15, "bold")).place(x=15, y=205)
Checkbutton(screen, text = "Reviews_Management", variable=reviews_management, font=("times new roman", 15, "bold")).place(x=15, y=225)
Checkbutton(screen, text = "Publish History", variable=publish_history, font=("times new roman", 15, "bold")).place(x=15, y=245)
Checkbutton(screen, text = "Hierarchy Details", variable=hierarchy_details, font=("times new roman", 15, "bold")).place(x=15, y=265)
Checkbutton(screen, text = "NPS Trend", variable=nps_trend, font=("times new roman", 15, "bold")).place(x=15, y=285)
Checkbutton(screen, text = "Account Statistics", variable=account_statistics, font=("times new roman", 15, "bold")).place(x=15, y=305)
Checkbutton(screen, text = "SMS Delivery", variable=sms_delivery, font=("times new roman", 15, "bold")).place(x=15, y=325)
Checkbutton(screen, text = "Survey Email", variable=survey_email, font=("times new roman", 15, "bold")).place(x=15, y=345)
Checkbutton(screen, text = "Verified Users", variable=verified_users, font=("times new roman", 15, "bold")).place(x=15, y=365)
Checkbutton(screen, text = "NPS", variable=nps, font=("times new roman", 15, "bold")).place(x=15, y=385)
Checkbutton(screen, text = "Ranking Tier", variable=ranking_tier, font=("times new roman", 15, "bold")).place(x=15, y=405)
Checkbutton(screen, text = "Incomplete Survey", variable=incomplete_survey, font=("times new roman", 15, "bold")).place(x=15, y=425)
Checkbutton(screen, text = "Survey Statistics", variable=survey_statistics, font=("times new roman", 15, "bold")).place(x=15, y=445)


# Button(screen, text='Calendar', command=calendar_view).place(x=15, y=220)
Label(text= "Report start date", fg='magenta', font=("times new roman", 15, "bold")).place(x=15, y=480)
Button(screen, text='Start date', command=dateentry_view_start_date,  highlightbackground='#e0ffff',  font=("times new roman", 15, "bold")).place(x=15, y=500)
Label(text= "Report end date", fg='magenta', font=("times new roman", 15, "bold")).place(x=15, y=535)
Button(screen, text='End date', command=dateentry_view_end_date, highlightbackground='#e0ffff', font=("times new roman", 15, "bold")).place(x=15, y=555)

Label(text="Choose environment *", fg='magenta', font=("times new roman", 15, "bold")).place(x=15, y=590)
Checkbutton(screen, text = "Sandbox", variable=sandbox, font=("times new roman", 15, "bold")).place(x=15, y=615)
Checkbutton(screen, text = "Production", variable=production, font=("times new roman", 15, "bold")).place(x=100, y=615)


Button(screen, text="Submit", width="14", bg="white", highlightbackground="#98fb98", command=register_user, font=("times new roman", 15, "bold")).place(x=15, y=650)
screen.mainloop()
