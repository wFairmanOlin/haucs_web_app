

from datetime import datetime, timedelta, timezone
import firebase
import json
import os
from firebase_admin import db
import numpy as np


fb_key = os.getenv('fb_key')

if fb_key:
    deployed = True
else:
    deployed = False
    with open('fb_key.json', 'r') as file:
        fb_key = file.read()

fb_app = firebase.login(fb_key)

with open('static/json/farm_features.json', 'r') as file:
    data = json.load(file)

pids = [str(i['properties']['number']) for i in data['features']]
last_do = dict()
curr_time = datetime.now(timezone.utc)
scurrent = (curr_time - timedelta(days=1)).strftime('%Y%m%d_%H:%M:%S')
for pid in pids:
    pdata = db.reference('LH_Farm/pond_' + pid).order_by_key().start_at(scurrent).limit_to_last(1).get()
    if pdata:
        for i in pdata:
            do = np.array(pdata[i]['do']).astype('float')
            init_do = float(pdata[i]['init_do'])
            last_do['pond_' + pid] = {'last_do': 100 * do[do > 0].mean() / init_do}
    else:
        last_do['pond_' + pid] = {'last_do': -1}

db.reference("LH_Farm/overview").set(last_do)
print("updated overview")