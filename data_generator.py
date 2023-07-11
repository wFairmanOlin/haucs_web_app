import time
from datetime import datetime
from datetime import timedelta
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import numpy as np

# define number of ponds
num_ponds = 70
# define lower left point of map
base_lat = 37.699912
base_lng = -89.471409
# define width and height of map
map_width = 0.026387
map_height = 0.009554
# define start time
generator_time = datetime(2023, 7, 4, hour=1, minute=0)
# define timeout
timeout = 60 * 60

def get_message():
    message = {}
    #generate position
    message['lat'] = float(np.round(base_lat + np.random.random(1) * map_height, 6)[0])
    message['lng'] = float(np.round(base_lng + np.random.random(1) * map_width, 6)[0])
    message['heading'] = int(np.random.randint(0, 360))
    # generate initial above water sensor values
    message['init_pressure'] = int(np.round(np.random.normal(1013, 10)))
    message['init_do'] = int(np.round(np.random.normal(32, 5)))
    # generate below water sensor values
    # get number of samles
    x = np.random.random()
    if x > 0.95:
        n_samples = 3
    elif x > 0.8:
        n_samples = 2
    else:
        n_samples = 1
    do = [int(np.random.normal(100, 40)) for i in range(n_samples)]
    hpa = [int(np.random.randint(1020, 1090)) for i in range(n_samples)]
    temp = [float(np.round(np.random.normal(20, 6), 2)) for i in range(n_samples)]
    message['do'] = do
    message['pressure'] = hpa
    message['temp'] = temp

    return message

def get_do(message):
    p = np.array(message['pressure'])
    idx = np.where(p == p.max())
    return message['do'][idx[0][0]]

if __name__ == "__main__":
    #initialize firebase
    try:
        print(cred)
    except:
        cred = credentials.Certificate("fb_key.json")
        app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://haucs-monitoring-default-rtdb.firebaseio.com'})

    ref = db.reference('/LH_Farm')
    upload_rate = 1 #seconds

    timeout += time.time()
    last_update = 0
    while (time.time() < timeout):
        # send a message
        if time.time() >= (last_update + upload_rate):
            last_update = time.time()
            #set reference to pond
            pond_id = str(np.random.randint(1, num_ponds + 1)) #upper limit is exclusive
            pond_ref = ref.child("pond_" + pond_id)
            #get a timestamp
            generator_time += timedelta(minutes=np.random.randint(1, 3))
            message_time = generator_time.strftime('%Y%m%d_%H:%M:%S')
            #get a message
            message = get_message()
            #send message
            pond_ref.child(message_time).set(message)

            #update overview branch
            p_overview_ref = ref.child("overview/pond_" + pond_id)
            do = get_do(message)
            p_overview_ref.child('last_do').set(do)
            print(message_time, pond_id, message)

    #finish
    firebase_admin.delete_app(app)
