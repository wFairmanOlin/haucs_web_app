import json
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import pytz

def login(key_path):
    """
    Start a Firebase Instance

    return: an app instance
    """
    cred = credentials.Certificate(key_path)
    return firebase_admin.initialize_app(cred, {'databaseURL': 'https://haucs-monitoring-default-rtdb.firebaseio.com'})

def logout(app):
    """
    Logout of a Firebase Instance
    """
    firebase_admin.delete_app(app)

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

    def __init__(self, name):
        ref = db.reference('/' + name)
        data = ref.get()
        self.d_dt = to_datetime(data['data'])
        self.s_dt = to_datetime(data['status'])
        self.on = np.array([int(data['data'][i][1]) for i in data['data']])
        self.off = np.array([int(data['data'][i][0]) for i in data['data']])
        self.g = np.array([int(data['data'][i][2]) for i in data['data']])
        self.battv = np.array([float(data['status'][i]['batt_v']) for i in data['status']])
        self.id = int(name[-1])

    def plot_timeseries(self, mv=3):
        # Set date format for x-axis labels
        date_fmt = '%m-%d %H:%M'
        # Use DateFormatter to set the data to the correct format.
        date_formatter = mdates.DateFormatter(date_fmt, tz=(pytz.timezone("US/Eastern")))
        lower = self.d_dt[-1] - timedelta(days=7)

        window = self.d_dt > lower

        plt.figure()
        plt.plot(self.d_dt[window], moving_average(self.on[window] - self.off[window], mv))
        # plt.xlim(lower, upper)
        # plt.ylim(0, 150)
        plt.title("Sensor " + str(self.id) + " Diff Weekly")
        plt.ylabel("Sensor On - Off")
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.savefig("static/"+ str(self.id) + "_timeseries.png")

if __name__ == "__main__":

    app = login("fb_key.json")

    logout(app)
