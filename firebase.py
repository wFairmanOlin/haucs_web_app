import json
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import pytz
matplotlib.use('agg')

def login(key_dict):
    """
    Start a Firebase Instance

    return: an app instance
    """
    data = json.loads(key_dict)
    cred = credentials.Certificate(data)
    return firebase_admin.initialize_app(cred, {'databaseURL': 'https://haucs-monitoring-default-rtdb.firebaseio.com'})

def logout(app):
    """
    Logout of a Firebase Instance
    """
    firebase_admin.delete_app(app)

def restart_firebase(app, key_dict):
    firebase_admin.delete_app(app)
    time.sleep(10)
    new_app = login(key_dict)
    return new_app

def moving_average(x, n):
    """
    Simple moving average filter
    """
    filter = np.ones(n) / n
    return np.convolve(x, filter, 'same')

def to_datetime(dates, tz_aware=True):
    """
    Standardizes the various types of string datetime formats
    """
    dt = []
    for i in dates:
        i = i.replace('T','_')
        i = i.replace('-','')
        i = i.replace(' ', '_')
        try:
            i_dt = datetime.strptime(i, '%Y%m%d_%H:%M:%S')
        except:
            print(i)
        if tz_aware:
            tz = pytz.timezone('US/Eastern')
            i_dt = tz.localize(i_dt)

        dt.append(i_dt)
    return np.array(dt)

class bmass_sensor():

    def __init__(self, name, n):
        ref_data = db.reference('/bmass_' + str(name) + '/data')
        ref_status = db.reference('/bmass_' + str(name) + '/status')
        data = dict()
        data['data'] = ref_data.order_by_key().limit_to_last(n).get()
        data['status'] = ref_status.order_by_key().limit_to_last(n).get()
        self.d_dt = to_datetime(data['data'])
        self.s_dt = to_datetime(data['status'])
        self.on = np.array([int(data['data'][i][1]) for i in data['data']])
        self.off = np.array([int(data['data'][i][0]) for i in data['data']])
        self.g = np.array([int(data['data'][i][2]) for i in data['data']])
        self.battv = np.array([float(data['status'][i]['batt_v']) for i in data['status']])
        self.id = int(name)

    def plot_timeseries(self, mv=3):
        # Set date format for x-axis labels
        date_fmt = '%m-%d %H:%M'
        # Use DateFormatter to set the data to the correct format.
        date_formatter = mdates.DateFormatter(date_fmt, tz=(pytz.timezone("US/Eastern")))
        lower = self.d_dt[-1] - timedelta(days=7)

        window = self.d_dt > lower

        plt.figure()
        plt.plot(self.d_dt[window], moving_average(self.on[window] - self.off[window], mv))
        plt.title("Sensor " + str(self.id) + " Diff Weekly")
        plt.ylabel("Sensor On - Off")
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.savefig("static/"+ str(self.id) + "_timeseries.png")

class pond():

    def __init__(self, name, n):
        ref = db.reference('/LH_Farm/pond_' + str(name))
        data = ref.order_by_key().limit_to_last(n).get()
        final_pressure=[]
        final_do = []
        final_temp = []

        for i in data:
            pressure = data[i]['pressure']
            do = data[i]['do']
            temp = data[i]['temp']
            high_pressure = max(pressure)
            index_hp = pressure.index(high_pressure)
            final_pressure.append(pressure[index_hp])
            final_do.append(do[index_hp])
            final_temp.append(temp[index_hp])
        
        self.d_dt = to_datetime(data)
        self.heading = np.array([(data[i]['heading']) for i in data])
        self.init_do = np.array([(data[i]['init_do']) for i in data])
        self.init_pressure = np.array([(data[i]['init_pressure']) for i in data])
        self.lat = np.array([(data[i]['lat']) for i in data])
        self.lng = np.array([(data[i]['lng']) for i in data])
        self.pressure = np.array(final_pressure)
        self.do = np.array(final_do)
        self.temp = np.array(final_temp)
        self.id = int(name)
    
    # def plot_do(self, mv=10):
    #     # Set date format for x-axis labels
    #     date_fmt = '%m-%d %H:%M'
    #     # Use DateFormatter to set the data to the correct format.
    #     date_formatter = mdates.DateFormatter(date_fmt, tz=(pytz.timezone("US/Eastern")))
    #     lower = self.d_dt[-1] - timedelta(hours=24)

    #     window = self.d_dt > lower

    #     plt.figure()
    #     plt.plot(self.d_dt[window], moving_average(self.pressure[window] - self.init_pressure[window], mv))
    #     plt.title("Dissolved Oxygen " + str(self.id) + " Diff Daily")
    #     plt.ylabel("DO (%)")
    #     plt.gcf().autofmt_xdate()
    #     plt.gca().xaxis.set_major_formatter(date_formatter)
    #     plt.savefig("static/"+ str(self.id) + "_do_graph.png")
    
if __name__ == "__main__":

    app = login("fb_key.json")

    logout(app)
