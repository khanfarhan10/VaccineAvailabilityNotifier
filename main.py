"""
python app.py
"""
from vaccine_availability import getSlots, convert_to_str, send_mail

if __name__ == '__main__':
    flag_available, Available_Slots = getSlots(DIST_ID = 446, numdays = 20, age = 21)
    msg = "No available slots found"

    body = convert_to_str(Available_Slots) if len(Available_Slots) > 0 else msg
    MAILS = ['swaymsdennings@gmail.com', 'njrfarhandasilva10@gmail.com']

    for mail in MAILS:
        send_mail(body, receiver_email=mail,
                  subject='VACCINE AVAILABILITY NOTIFICATION')
