from flask import Flask, render_template, url_for, request, redirect 
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import firebase

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/analytics',methods=['GET'])
def dropdown():
    num_ponds = 5
    ponds = range(1,num_ponds+1)
    return render_template('analytics.html',ponds=ponds)

@app.route('/sensor/<int:sensor_id>')
def show_sensor(sensor_id):
    return render_template('sensor.html', sensor_id=sensor_id)

@app.route('/index')
def map():
    return render_template('index.html')

def init_firebase():
    """
    Generate Images on Startup
    """
    fb_app = firebase.login("fb_key.json")

    for id in range(1, 6):
        bmx = firebase.bmass_sensor('bmass_' + str(id))
        bmx.plot_timeseries(mv=10)
    firebase.logout(fb_app)

if __name__ == "__main__":
    init_firebase()
    app.run(debug=True)
