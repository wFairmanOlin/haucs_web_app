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
########## FUNCTIONS ################
def convert_to_mgl(do, t, p, s=0):
    '''
    do: dissolved oxygen in percent saturation
    t: temperature in celcius
    p: pressure in hPa
    s: salinity in parts per thousand
    '''
    T = t + 273.15 #temperature in kelvin
    P = p * 9.869233e-4 #pressure in atm

    DO_baseline = np.exp(-139.34411 + 1.575701e5/T - 6.642308e7/np.power(T, 2) + 1.2438e10/np.power(T, 3) - 8.621949e11/np.power(T, 4))
    # SALINITY CORRECTION
    Fs = np.exp(-s * (0.017674 - 10.754/T + 2140.7/np.power(T, 2)))
    # PRESSURE CORRECTION
    theta = 0.000975 - 1.426e-5 * t + 6.436e-8 * np.power(t, 2)
    u = np.exp(11.8571 - 3840.7/T - 216961/np.power(T, 2))
    Fp = (P - u) * (1 - theta * P) / (1 - u) / (1 - theta)

    DO_corrected = DO_baseline * Fs * Fp

    DO_mgl = do / 100 * DO_corrected

    return DO_mgl

def send_email(subject, body, recipient_list, pond_id=""):

    recipients = db.reference('LH_Farm/email/' +  recipient_list).get()
    recipients = [i for i in recipients if i != None]
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = cred['from']
    msg['To'] = ', '.join(recipients)


    content = f"{datetime.now(pytz.timezone('US/Central')).strftime('%I:%M %p')} CT\n"
    content += body
    if pond_id:
        content += "\nhttp://www.sailhboi.com/pond" + pond_id
    msg.set_content(content)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(cred['user'], cred['pwd'])
        server.send_message(msg)
        server.close()
    except:
        print("failed to send email")

def check_trucks():
    do_send = False
    do_update = False
    recipient_list = "truck_notifications"
    tbase_hbeat = db.reference("LH_Farm/equipment/truck_basestation").get()
    last_hbeat = time.time() - tbase_hbeat['time']
    #if updated within 30 minutes
    if last_hbeat < 60*30:
        if tbase_hbeat.get('flagged') == 1:
            content = 'truck basestation is operational'
            tbase_hbeat['flagged'] = 0
            do_send = True
            do_update = True
        elif not tbase_hbeat.get('flagged'):
            tbase_hbeat['flagged'] = 0
            do_update = True
    #if not updated within 30 minutes
    else:
        if not (tbase_hbeat.get('flagged') == 1):
            content = f"truck basestation has been offline for {last_hbeat // 60} minutes"
            tbase_hbeat['flagged'] = 1
            do_send = True
            do_update = True

    if do_send:
        send_email('TRUCK BASESTATION', content, recipient_list)
    if do_update:
        db.reference("LH_Farm/equipment/truck_basestation").set(tbase_hbeat)

def check_ponds():
    recipient_list = "buoy_notifications"
    with open('static/json/farm_features.json', 'r') as file:
        data = json.load(file)

    pids = [str(i['properties']['number']) for i in data['features']]
    last_do = dict()
    curr_time = datetime.now(timezone.utc)
    day_delay = (curr_time - timedelta(days=1)).strftime('%Y%m%d_%H:%M:%S')
    hour_delay = (curr_time - timedelta(hours=1)).strftime('%Y%m%d_%H:%M:%S')

    for pid in pids:
        #update overview
        pdata = db.reference('LH_Farm/pond_' + pid).order_by_key().start_at(day_delay).limit_to_last(1).get()
        if pdata:
            for i in pdata:
                do = np.array(pdata[i]['do']).astype('float')
                t = np.array(pdata[i]['temp']).astype('float')
                init_p = pdata[i]['init_pressure']
                init_do = float(pdata[i]['init_do'])
                do_level = 100 * do[do > 0].mean() / init_do
                last_do['pond_' + pid] = {'last_do': do_level}
                #notifications
                #only test data within past hour from buoys
                if (i > hour_delay) and (pdata[i]['type'] == 'buoy'):
                    do_mgl = convert_to_mgl(do_level, np.mean(t), init_p)
                    pond_stats = db.reference('LH_Farm/overview/pond_' + pid).get()
                    DO_ALERT_VALUE = db.reference('LH_Farm/email/do_alert').get()
                    BUOY_ALERT_FREQUENCY = db.reference('LH_Farm/email/buoy_alert_frequency').get()
                    #create dictionary if new
                    if not pond_stats:
                        pond_stats = dict()
                    #get last notification time
                    last_message = pond_stats.get('last_notification')
                    if not last_message:
                        last_message = time.time() - BUOY_ALERT_FREQUENCY * 60
                    #send email if unmuted and 1 hour has passed
                    if not pond_stats.get('mute'):
                        if do_level < DO_ALERT_VALUE:
                            if (time.time() - last_message) >= BUOY_ALERT_FREQUENCY * 60:
                                pond_stats['last_notification'] = time.time()
                                contents = f"DO measured at {round(do_mgl, 2)}mg/l ({round(do_level)}%)\nNABuoy {pdata[i]['sid']}"
                                send_email(f"LOW DO POND {pid}", contents, recipient_list, pid)
                    pond_stats['last_do'] = do_level
                    last_do['pond_' + pid] = pond_stats
        else:
            last_do['pond_' + pid] = {'last_do': -1}

    db.reference("LH_Farm/overview").set(last_do)
    print("updated overview")

check_trucks()
check_ponds()