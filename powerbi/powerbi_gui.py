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
screen.geometry("650x650")
screen.resizable(False, False)
screen.title("PowerBI auth form")
error_window = False
start_date = None
end_date = None

def database():
    conn = sqlite3.connect('database.db')
    connection = conn.cursor()
    connection.execute("CREATE TABLE IF NOT EXISTS powertbl(id integer primary key autoincrement, name TEXT, password TEXT, start_date TEXT, end_date TEXT, reports TEXT, created_at DATETIME NOT NULL)")
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
    # import pdb; pdb.set_trace()
    """after successfull verification saving the user"""
    global error_window
    username_text = username.get()
    password_text = password.get()
    user_exists = None

    if not username_text or not password_text:
        if not error_window:
            error_window_screen("190x120", "All fields are required")
    elif username_text and len(username_text) < 4:
        if not error_window:
            error_window_screen("290x120", "username must be at least 4 characters")        
    else:
        user_exists = user_name_check()
        if not user_exists:
            if not error_window:
                error_window_screen("190x120", "username already exists")  
        if len(password_text) < 6:
            if not error_window:
                error_window_screen("290x120", "password must be at least 6 characters")
        elif re.search('[0-9]', password_text) is None:
            if not error_window:
                error_window_screen("340x120", "make sure password, has at least a number in it")
        elif re.search('[A-Z]', password_text) is None:
            if not error_window:
                error_window_screen("340x120", "make sure password, has at least a capital letter in it")
        else:
            hashed_password = password_hash(password_text)
            save_data(hashed_password)




def save_data(hashed_password):
    global start_date
    global end_date
    total_reports = {}
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
    """adding user details to the database"""
    try:
        conn = sqlite3.connect("database.db")
        connection = conn.cursor()
        utc_date_time = datetime.utcnow()
        current_date = datetime.strftime(utc_date_time, "%Y-%m-%d")
        created_at = datetime.strftime(utc_date_time, "%Y-%m-%d %H:%M:%S")
        start_date = start_date if start_date else current_date
        end_date = end_date if end_date else current_date
        connection.execute('INSERT INTO powertbl(name, password, start_date, end_date, reports, created_at) VALUES(?,?,?,?,?,?)', (username.get(), hashed_password, start_date, end_date, json.dumps(total_reports), created_at))
        conn.commit()
        success()
    except Exception as err:
        pass


# def get_date():
#     start_date.config(text=start_calender.get_date())

# def calendar_view():
#     def print_sel():
#         print(cal.selection_get())

#     top = tk.Toplevel(screen)

#     cal = Calendar(top,
#                    font="Arial 14", selectmode='day',
#                    cursor="hand1", year=2018, month=2, day=5)
#     cal.pack(fill="both", expand=True)
#     Button(top, text="ok", command=lambda: print_sel).pack()

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


heading = Label(text="PowerBI authorization form", fg="black", bg="grey", width="500", height="3").pack()

Label(text= "Username * ").place(x=15, y=70)
Label(text= "Password * ").place(x=17, y=125)

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

Entry(screen, textvariable=username).place(x=15, y=95)
Entry(screen, textvariable=password, show="*").place(x=15, y=145)

# start_date = Button(screen, text="Choose start date", command=get_date).place(x=15, y=200)
# Label(screen, text="").place(x=15, y=140)
# start_calender = Calendar(screen, selectmode="day", year=2021, month=10, day=22)
# start_calender.pack(pady=20)

# checkboxes
Label(text= "Choose Report/Reports * ").place(x=15, y=180)
Checkbutton(screen, text = "Survey Results", variable=survey_results).place(x=15, y=205)
Checkbutton(screen, text = "Reviews_Management", variable=reviews_management).place(x=15, y=225)
Checkbutton(screen, text = "Publish History", variable=publish_history).place(x=15, y=245)
Checkbutton(screen, text = "Hierarchy Details", variable=hierarchy_details).place(x=15, y=265)
Checkbutton(screen, text = "NPS Trend", variable=nps_trend).place(x=15, y=285)
Checkbutton(screen, text = "Account Statistics", variable=account_statistics).place(x=15, y=305)
Checkbutton(screen, text = "SMS Delivery", variable=sms_delivery).place(x=15, y=325)
Checkbutton(screen, text = "Survey Email", variable=survey_email).place(x=15, y=345)
Checkbutton(screen, text = "Verified Users", variable=verified_users).place(x=15, y=365)
Checkbutton(screen, text = "NPS", variable=nps).place(x=15, y=385)
Checkbutton(screen, text = "Ranking Tier", variable=ranking_tier).place(x=15, y=405)
Checkbutton(screen, text = "Incomplete Survey", variable=incomplete_survey).place(x=15, y=425)
Checkbutton(screen, text = "Survey Statistics", variable=survey_statistics).place(x=15, y=445)


# Button(screen, text='Calendar', command=calendar_view).place(x=15, y=220)
Label(text= "Report start date").place(x=15, y=480)
Button(screen, text='Start date', command=dateentry_view_start_date).place(x=15, y=500)
Label(text= "Report end date").place(x=15, y=535)
Button(screen, text='End date', command=dateentry_view_end_date).place(x=15, y=555)


Button(screen, text="Submit", width="14", bg="grey", command=register_user).place(x=15, y=600)
screen.mainloop()
