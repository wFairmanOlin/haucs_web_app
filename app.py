from flask import Flask, render_template, url_for, request, redirect 
from datetime import datetime
import firebase
import json
import os


fb_key = os.getenv('fb_key')

if fb_key:
    print("running in deployment mode")
    deployed = True
else:
    print("running in debug mode")
    deployed = False
    with open('fb_key.json', 'r') as file:
        fb_key = file.read()

def load_data():
    fb_app = firebase.login(fb_key)

    bms = dict()
    num_sensors=5
    for i in range(1, num_sensors + 1):
        bms['bmass_'+str(i)] = firebase.bmass_sensor('bmass_'+str(i))

    last_battv=dict()
    for j in bms:
        last_battv[bms[j].id] = bms[j].battv[-1]
    firebase.logout(fb_app)
    
    return bms, last_battv

def generate_graphs():
    bms = load_data()
    for i in bms:
        bms[i].plot_timeseries(mv=10)


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/HAUCS')
def haucs():
    bms, last_battv = load_data()
    with open('static/json/farm_features.json', 'r') as file:
        data = file.read()
    
    return render_template('HAUCS.html', data=data, battv=json.dumps(last_battv))

@app.route('/biomass')
def map():
    # get data
    bms, last_battv = load_data()
    # generate_graphs
    for i in bms:
        bms[i].plot_timeseries(mv=10)

    with open('static/json/tanks_features.json', 'r') as file:
        data = file.read()

    return render_template('biomass.html', data=data,battv=json.dumps(last_battv))

@app.route('/sensor'+'<int:sensor_id>')
def show_sensor(sensor_id):
    bms, last_battv = load_data()
    return render_template('tanks_analytics.html', sensor_id=sensor_id, last_battv=last_battv)

@app.route('/pond'+'<int:pond_id>')
def show_pond(pond_id):
    bms, last_battv = load_data()
    return render_template('haucs_analytics.html', pond_id=pond_id, last_battv = last_battv)

if __name__ == "__main__":
    if not deployed:
        app.run(debug=True)
    
