"""
python app.py
"""

from flask import Flask, render_template, request, url_for, send_from_directory, jsonify, send_file
import os
from vaccine_availability import getSlots, convert_to_str, send_mail


# "templates" this is for plain html files or "Great_Templates" this is for complex css + imgs +js +html+sass
TEMPLATES = "templates"

app = Flask(__name__, static_folder="assets", template_folder=TEMPLATES)
ROOT_DIR = os.getcwd()

# Reloading
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
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


