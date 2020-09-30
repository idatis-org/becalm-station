# This file is part of becalm-station
# https://github.com/idatis-org/becalm-station
# Copyright: Copyright (C) 2020 Enrique Melero <enrique.melero@gmail.com>
# License:   Apache License Version 2.0, January 2004
#            The full text of the Apache License is available here
#            http://www.apache.org/licenses/

from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import json
from flask_apscheduler import APScheduler

# The Server hostname and port where we can contact the becalm server service
serverAddr="localhost"
serverPort="8080"

# The becalm Station hostname and port where the sensor drivers are running
sensorAddr="localhost"
sensorPort="8887"

# URL or the becalm Server to post the results
# There is normally no need to change this
serverurl="http://" + serverAddr + ":" + serverPort + "/v100/data-sensor/2?id_device=1"
sensorurl="http://" + sensorAddr + ":" + sensorPort + "/"

scheduler = APScheduler()


@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=10)
def job1():
    with scheduler.app.app_context():

        # Gather data from sensor microsercice
        r = requests.get(sensorurl)

    if r.status_code != 200:
        print("Error reading sensor " + sensorurl)
        return

    payload_dict = r.json()
    timestamp= datetime.now().__str__()
    payload=[]
    for key in payload_dict.keys():
        measure={
            'measure_type': key,
            'measure_value': payload_dict[key],
            'date_generation': timestamp
        }
        payload.append(measure)


# Post results to central server
    headers = {'Content-type': 'application/json'}
    r = requests.post(serverurl, headers=headers, json=payload)

    if r.status_code == 201:
        print ( datetime.now().__str__() + " Posted to server")
    else:
        print ("Error posting to server: " + str(r.status_code))


app = Flask(__name__)


@app.route('/rest/api/v1.0/debug', methods=['GET'])
def home2():
    r = requests.get(sensorurl + '/debug')
    return  r.json()

if __name__ == '__main__':
   scheduler.api_enabled = True
   scheduler.init_app(app)
   scheduler.start()
   app.run(debug = True,host='0.0.0.0', port=8081)
