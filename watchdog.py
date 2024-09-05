from datetime import datetime, timedelta, timezone
import firebase
import os, smtplib, json, time
from firebase_admin import db
import numpy as np
from email.message import EmailMessage
import pytz

fb_key = os.getenv('fb_key')

if fb_key:
    deployed = True
else:
    deployed = False
    with open('fb_key.json', 'r') as file:
        fb_key = file.read()

fb_app = firebase.login(fb_key)

cred = db.reference('LH_Farm/email/credentials').get()
cred['to'] = db.reference('LH_Farm/email/truck_notifications').get()

def send_email(body):

    msg = EmailMessage()
    msg['Subject'] = "HAUCS Watchdog" 
    msg['From'] = cred['from']
    msg['To'] = ', '.join(cred['to'])


    content = f"{datetime.now(pytz.timezone('US/Central')).strftime('%I:%M %p')}\n"
    content += body
    msg.set_content(content)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(cred['user'], cred['pwd'])
        server.send_message(msg)
        server.close()
    except:
        print("failed to send email")


##### MAIN CODE #####
#check status
tbase_hbeat = db.reference("LH_Farm/equipment/truck_basestation").get()
last_hbeat = time.time() - tbase_hbeat['time']

#if updated within 30 minutes
if last_hbeat < 60*30:
    if tbase_hbeat.get('flagged') == 1:
        tbase_hbeat['flagged'] = 0
        send_email('truck basestation is operational')
        db.reference("LH_Farm/equipment/truck_basestation").set(tbase_hbeat)
    elif not tbase_hbeat.get('flagged'):
        tbase_hbeat['flagged'] = 0
        db.reference("LH_Farm/equipment/truck_basestation").set(tbase_hbeat)
#if not updated within 30 minutes
else:
    if not (tbase_hbeat.get('flagged') == 1):
        tbase_hbeat['flagged'] = 1
        send_email(f'WARNING: truck basestation has been unresponsive for {int(last_hbeat // 60)} minutes')
        db.reference("LH_Farm/equipment/truck_basestation").set(tbase_hbeat)
