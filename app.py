from flask import Flask, render_template, url_for, request, redirect 
from datetime import datetime
import firebase
import json 
import data_generator

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/HAUCS')
def haucs():
    with open('static/json/farm_features.json', 'r') as file:
        data = file.read()
    
    return render_template('HAUCS.html', data=data, battv=json.dumps(last_battv))

@app.route('/biomass')
def map():
    with open('static/json/tanks_features.json', 'r') as file:
        data = file.read()

    return render_template('biomass.html', data=data,battv=json.dumps(last_battv))

@app.route('/sensor'+'<int:sensor_id>')
def show_sensor(sensor_id):
    return render_template('sensor.html', sensor_id=sensor_id)

if __name__ == "__main__":
    print("starting init")
    fb_app = firebase.login("fb_key.json")

    bms = dict()
    num_sensors=5
    for i in range(1, num_sensors + 1):
        bms['bmass_'+str(i)] = firebase.bmass_sensor('bmass_'+str(i))
    
    for i in bms:
        bms[i].plot_timeseries(mv=10)

    last_battv=dict()
    for j in bms:
        last_battv[bms[j].id] = bms[j].battv[-1]
    

    firebase.logout(fb_app)
    app.run(debug=False)
    print('finishing init')
