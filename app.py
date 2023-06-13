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
def analytics():
    '''num_ponds = 5
    list=range(1,num_ponds+1)'''
    return render_template('analytics.html')
def dropdown():
    num_ponds = 5
    ponds = range(1,num_ponds+1)
    
    return render_template('analytics.html',ponds=ponds)



'''@app.route('/bmass/<bm2>')
def bmass(firebase.bm2):
    return render_template('')'''

@app.route('/sensor/<int:sensor_id>')
def show_sensor(sensor_id):
    return render_template('sensor.html', sensor_id=sensor_id)


if __name__ == "__main__":
    app.run(debug=True)

    fb_app = firebase.login("fb_key.json")
    firebase.logout(fb_app)