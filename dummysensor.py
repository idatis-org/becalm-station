#!/usr/bin/python
from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

class dummysensor:
    heartbeat=60
    SpO2=2000

    def read_heartbeat(self):
        return self.heartbeat

    def read_SpO2(self):
        return self.SpO2

sensor = dummysensor()
@app.route('/rest/api/v1.0/heartbeat', methods=['GET'])
def get_tasks():
    return str(sensor.read_heartbeat())

@app.route('/rest/api/v1.0/spo2', methods=['GET'])
def get_val2():
    return str(sensor.read_SpO2() )


@app.route('/debug', methods=['GET'])
def debug():
    max30100= dict()
    max30100['h'] = sensor.read_heartbeat()
    max30100['o'] = sensor.read_SpO2()
    return max30100

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8887)

