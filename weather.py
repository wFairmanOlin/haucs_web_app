import urllib.request
import json
import time
from datetime import datetime, timedelta, timezone
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pytz
import os

matplotlib.use('agg')


def generate_weather(duration=2):
    start = str(round(time.time() * 1000) -  duration * 24 * 60 * 60  * 1000) #10 minutes
    end = str(round(time.time() * 1000))

    # FETCH DATA
    with urllib.request.urlopen('https://api.sensestream.org/observations/measurements/hboi_aqua_2/0?start=' + start + '&end=' + end) as response:
        data = json.load(response)

    # CONVERT DATA
    if data['errorCode'] == 0:

        dt = [datetime.fromtimestamp(i['time'] / 1000, timezone.utc) for i in data['result']]
        temp = [32 + (9 / 5 * i['readings'][7]) for i in data['result']]
        wind_dir = [i['readings'][2] for i in data['result']]
        wind_spd = [i['readings'][5] for i in data['result']]
        rain = [i['readings'][12] for i in data['result']]
        solar_rad = [i['readings'][18] for i in data['result']]
        baro = [i['readings'][0] for i in data['result']]
        rh = [i['readings'][9] for i in data['result']]

        date_fmt = '%m/%d %I %p'
        # Use DateFormatter to set the data to the correct format.
        date_formatter = mdates.DateFormatter(date_fmt, tz=(pytz.timezone("US/Central")))

        # PLOT DATA

        plt.figure(figsize=(8, 5))
        plt.plot(dt, temp, linewidth=3)
        plt.ylabel("Air temperature (°F)", fontsize=12)
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.savefig("static/graphs/haucs/weather_temp.png")

        plt.figure(figsize=(8,5))
        plt.subplot(2,1,1)
        plt.plot(dt, wind_spd, linewidth=2)
        plt.ylabel("Wind Speed (m/s)", fontsize=12)
        plt.subplot(2,1,2)
        plt.plot(dt, wind_dir, color='r')
        plt.ylabel("Wind Dir. (deg)", fontsize=12)
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.savefig("static/graphs/haucs/weather_wind.png")

        plt.figure(figsize=(8, 5))
        plt.plot(dt, rain, linewidth=3)
        plt.ylabel("Rain Intensity (mm/h)", fontsize=12)
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.savefig("static/graphs/haucs/weather_rain.png")

        plt.figure(figsize=(8, 5))
        plt.plot(dt, solar_rad, linewidth=2)
        plt.ylabel("Solar Radiation (W/$m^2$)", fontsize=12)
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.savefig("static/graphs/haucs/weather_solar.png")

        plt.figure(figsize=(8, 5))
        plt.plot(dt, baro, linewidth=2)
        plt.ylabel("Barometric Pressure (hPa)", fontsize=12)
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.savefig("static/graphs/haucs/weather_baro.png")

        plt.figure(figsize=(8, 5))
        plt.plot(dt, rh, linewidth=2)
        plt.ylabel("Relative Humiditiy (%)", fontsize=12)
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.savefig("static/graphs/haucs/weather_rh.png")
