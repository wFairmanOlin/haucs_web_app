from flask import Flask, render_template, url_for, request, redirect 
from datetime import datetime
import firebase
import json 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/analytics',methods=['GET'])
def map():
    with open('static/json/map_features.json', 'r') as file:
        data = file.read()

    return render_template('analytics.html', data=data,battv=json.dumps(last_battv))

@app.route('/sensor'+'<int:sensor_id>')
def show_sensor(sensor_id):
    return render_template('sensor.html', sensor_id=sensor_id)

# def init_firebase():
#     """
#     Generate Images on Startup
#     """
    

if __name__ == "__main__":

    fb_app = firebase.login("fb_key.json")

    bms = dict()
    bms['bmass_1'] = firebase.bmass_sensor('bmass_1')
    bms['bmass_2'] = firebase.bmass_sensor('bmass_2')
    bms['bmass_3'] = firebase.bmass_sensor('bmass_3')
    bms['bmass_4'] = firebase.bmass_sensor('bmass_4')
    bms['bmass_5'] = firebase.bmass_sensor('bmass_5')

    for i in bms:
        bms[i].plot_timeseries(mv=10)

    last_battv=dict()
    for j in bms:
        last_battv[bms[j].id] = bms[j].battv[-1]

    firebase.logout(fb_app)
    # init_firebase()
    app.run(debug=True)
