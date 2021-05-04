"""
python app.py
"""

from flask import Flask, render_template, request, url_for, send_from_directory, jsonify, send_file
import os
from vaccine_availability import getSlots, convert_to_str, send_mail

from flask_apscheduler import APScheduler

scheduler = APScheduler()

def openTXT(path="userdata.txt"):
    with open(path) as f:
        data = f.readlines()
    return data

def openTXTSimple(path="userdata.txt"):
    with open(path) as f:
        data = f.read()
    return data

def writeTXT(line,path="userdata.txt"):
    with open(path, "a+") as f:
        f.write(line+"\n")

# for regular expressions
import re
 
# Make a regular expression
# for validating an Email
regex_mail = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

 
def isValidEmail(email):
 
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex_mail, email)):
        return True
 
    else:
        return False

# "templates" this is for plain html files or "Great_Templates" this is for complex css + imgs +js +html+sass
TEMPLATES = "templates"

app = Flask(__name__, static_folder="assets", template_folder=TEMPLATES)
ROOT_DIR = os.getcwd()

# Reloading
app.config['TEMPLATES_AUTO_RELOAD'] = True

def notify_user(mail = 'swaymsdennings@gmail.com',DIST_ID = 446, numdays = 20, age = 21):
    flag_available, Available_Slots = getSlots(DIST_ID, numdays, age)
    msg = "No available slots found"
    body = convert_to_str(Available_Slots) if len(Available_Slots) > 0 else msg
    body = body + "\nView the website now : https://www.cowin.gov.in/home"
    print(mail,body,"Sent!")
    cond  = len(Available_Slots) > 0 # True # len(Available_Slots) > 0
    if cond:
        send_mail(body, receiver_email=mail,subject='VACCINE AVAILABILITY NOTIFICATION')

def scheduleTask():
    data = openTXT()
    for each_line in data:
        emailid,districtid,age,days=each_line.split(",")
        districtid,age,days = int(districtid),int(age),int(days)
        notify_user(emailid,districtid,age,days)
    print("Scheduler Running")



@app.route('/')
def home():
    return render_template('index.html')

@app.route("/view",methods=['GET','POST'])
def download():
    uploads = app.root_path
    return send_from_directory(directory=uploads, filename="userdata.txt")


@app.route('/register', methods=["GET", "POST"])
def register():
    try:
        emailid = request.form["emailid"]
        districtid = int(request.form["districtid"])
        age = int(request.form["age"])
        days = int(request.form["days"])
        conds = request.form["conds"]
        
        print(emailid,districtid,age,days,conds)
        
        if not conds=="on" or not isValidEmail(emailid):
            raise ValueError('Terms and Conditions not met or Invalid Email ID.')
        line = emailid + "," + str(districtid) + "," + str(age) + "," + str(days)
        writeTXT(line)
        return render_template('register.html')
    except Exception as err:
        err_message = f"{err.__class__.__name__}: {err}"
        return "Incorrect Data Entered.\n" + err_message

"""
emailid,districtid,age,days= "njrfarhandasilva10@gmail.com",255,21,20
line = emailid + "," + str(districtid) + "," + str(age) + "," + str(days)
writeTXT(line)
emailid,districtid,age,days= "swaymsdennings@gmail.com",446,21,20
line = emailid + "," + str(districtid) + "," + str(age) + "," + str(days)
writeTXT(line)
"""


if __name__ == "__main__":
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", seconds=6000,max_instances=10) # 18000
    scheduler.start()
    app.run()
"""
if __name__ == '__main__':
    flag_available, Available_Slots = getSlots(DIST_ID=446, numdays=20, age=21)
    msg = "No available slots found"

    body = convert_to_str(Available_Slots) if len(Available_Slots) > 0 else msg
    MAILS = ['swaymsdennings@gmail.com', 'njrfarhandasilva10@gmail.com']

    for mail in MAILS:
        send_mail(body, receiver_email=mail,
                  subject='VACCINE AVAILABILITY NOTIFICATION')
"""
