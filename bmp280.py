#!/usr/bin/python3
# This file is part of becalm-station

# https://github.com/idatis-org/becalm-station
# Copyright: Copyright (C) 2020 Enrique Melero <enrique.melero@gmail.com>
# License:   Apache License Version 2.0, January 2004
#            The full text of the Apache License is available here
#            http://www.apache.org/licenses/

# -*- coding: utf-8 -*-

from flask import Flask, jsonify,send_from_directory, make_response 
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime
import board
import busio
import adafruit_bmp280
import json
import sqlite3 as sl
import os

# Some configurable variables
dbfile="becalm-station.db"


app = Flask(__name__, static_url_path='')

scheduler = BackgroundScheduler()
scheduler.start()

temperature = -1
pressureh = -1
pressurel = -1
lpressure= -1
lastmeasure = datetime.now()
lbreath= datetime.now()
linspiration=lbreath
rr = -1
ra = -1
tmpPhase=""
rtresh=0.1

def job1():

    global linspiration, lpressure, pressureh, pressurel,temperature, rr, lbreath, tmpPhase, ra
    tmpLapse=datetime.now() 
    temperature=bmp280.temperature
    tmpPressure=bmp280.pressure
    lastBreath=datetime.now()
    if pressurel==-1:
        pressurel=tmpPressure
    if pressureh==-1:
        pressureh=tmpPressure

    # Have we switched to inspire cycle?
    if tmpPressure < (pressureh+pressurel)/2 - rtresh :
        # Yes this is below the mid pression range
        # we can measure the breathing patterm (rate)
        # and we store the pression range between max and min
        if tmpPhase == 'E' :
            rr=60 / ( datetime.now() - linspiration ).total_seconds()
            lbreath=str(datetime.now()).split(".")[0]
            ra=pressureh-pressurel
            linspiration=datetime.now()

        # We are inspiring
        tmpPhase="I"

    # Have we switched to expire cycle?
    if tmpPressure > (pressureh+pressurel)/2 +rtresh :

        # If we were inspiring before
        # We measure the breathing rate
        # and the respiratory amplitude
        if tmpPhase == 'I' :   

            lbreath=datetime.now()
            ra=pressureh-pressurel
            tmpPhase="E"
    
    if tmpPhase=="E" :
        # measure pressure of expiration
        pressureh=tmpPressure

    if tmpPhase=="I" :
        # 
        pressurel=tmpPressure

    lpressure = tmpPressure
    lastmeasure = datetime.now()
    
    # Initalize database
    con = sl.connect(dbfile)
    con.execute('''PRAGMA synchronous = OFF''') 
    sql = 'INSERT INTO measure (type, value ) values(?, ?)'
    data = [
            ('t',temperature),
            ('p',lpressure),
            ('a',ra),
            ('q',pressurel),
            ('b',rr) 
            ]
    with con:
            con.executemany(sql, data)
            con.commit()

    print("Pressure:" + str(lpressure) + " bmp280 read lapse:" + str( ( lastmeasure - tmpLapse).total_seconds() ) )

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
bmp280.sea_level_pressure = 1013.25

# Initalize database
#con = sl.connect('becalm-station.db')

job = scheduler.add_job(job1, 'interval', seconds=0.3)

@app.route('/', methods=['GET'])
def data():
    # ('t', 'Temperature', '°C', 36, 40, 30, 50, 1),
    # ('p', 'Pressure in the mask', 'Pa', 100700, 101400, 100500, 101500, 1),
    # ('c', 'CO2 concentration', 'ppm', 110, 190, 100, 200, 0),
    # ('h', 'Heartbeat rate', 'beats/min', 110, 190, 100, 200, 0),
    # ('o', 'Sp02 - Oxygen saturation in blood', '?', 110, 185, 100, 200, 0),
    # ('a', 'Breath range', 'Pa', 110, 185, 100, 200, 0),
    # ('b', 'Breathing rate', 'respiraciones/minuto', 110, 185, 100, 200, 0),
    # ('q', 'PEEP', 'Pa', 110, 185, 100, 200, 0);
    output = dict()
    output['t'] = round(temperature,2)
    output['p'] = round(lpressure,2)
    output['a'] = round(ra, 2)
    #   output['Expire pressure'] = round(pressureh,2)
    output['q'] = round(pressurel,2)
    output['b'] = round(rr,2)
    #    output['Last breath'] = str(lbreath)
    #    output['Breathing phase'] = tmpPhase
    return(output)


@app.route('/debug', methods=['GET'])
def debug():
    output = dict()
    output['Temperature'] = round(temperature,2)
    output['Pressure'] = round(lpressure,2)
    output['Breath range'] = round(ra, 2)
    output['Expire pressure'] = round(pressureh,2)
    output['Inspire pressure'] = round(pressurel,2)
    output['Breathing rate'] = round(rr,2)
    output['Last breath'] = str(lbreath)
    output['Breathing phase'] = tmpPhase
    response=make_response(output,200)
    response.headers["Refresh"]=0.3
    return response


@app.route('/db', methods=['GET'])
def db():
    return send_from_directory(os.getcwd(),dbfile)
    

if __name__ == '__main__':

    # app.debug = True
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(host='0.0.0.0', port=8888, threaded=False, processes=1 )
