# TASK BERFORE RUN THIS PROGRAM
"""
1. Set environment variable for : 
1.1 FIREBASE_CREDENTIALS = Path of service account Firebase Admin
1.2 FIREBASE_DATABASE = URL Firebase Realtime Database
1.3 MQTT_SERVER = IP Address / URL Broker
1.4 MQTT_USER = Username MQTT Server (Not yet)
1.5 MQTT_PASS = Password MQTT Server (Not yet)

2.
"""

"""
Spacer (Task | Packages)
"""
# Import Packages
## Core
from flask import Flask, jsonify, request, abort
from flask_mqtt import Mqtt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

## System
import json
import os

"""
Spacer (Packages | Initialization)
"""
# Initialization
app = Flask(__name__)

## MQTT Server Configuration
app.config["MQTT_BROKER_URL"] = os.getenv("MQTT_SERVER") # IP Address or URL
app.config["MQTT_BROKER_PORT"] = 1883 # Port
app.config["MQTT_USERNAME"] = "" # Username authentication
app.config["MQTT_PASSWORD"] = "" # Password authentication
app.config["MQTT_KEEPALIVE"] = 5 # Time interval sending a ping to broker
app.config["MQTT_TLS_ENABLED"] = False # Change value to "True" if use TLS
mqtt_client = Mqtt(app)
topic = "smart_zero/"

## Firebase Admin
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
firebase_admin.initialize_app(cred, {"databaseURL":os.getenv("FIREBASE_DATABASE")})
data_db = db.reference("/")

"""
Spacer (Initialization | Routes)
"""
# Routes
## Index
@app.route("/", methods=["GET"])
def index():
    return data_db.get()
    
## Publish Data to Device
@app.route("/publish/<type>", methods=["POST"])
def publish(type):
    data_json = request.get_json()
    data_pub = {
        "slot":data_json["slot"],
        "status":data_json["status"]
    }
    
    if (type == "simple"):
        mqtt_client.publish(topic + data_json["id"], str(data_pub))
        
        return jsonify(
        {
            "message":"Device " + data_json["id"] + ", Slot " + str(data_json["slot"]),
            "status":data_json["status"]
        }
        )
        
    elif (type == "schedule"):
        """
        Example JSON
        {
        "id":"",
        "slot":[0,0],
        "schedule":{
                "day":[0, 0, 0, 0, 0, 0, 0],
                "start":["00:00", "00:00", "00:00", "00:00", "00:00", "00:00", "00:00"],
                "end":["00:00", "00:00", "00:00", "00:00", "00:00", "00:00", "00:00"]
            }
        }
        """
        
    else:
        return abort(404)

"""
Spacer (Routes | APP)
"""
# APP Run
if __name__ == "__main__":
    app.run(port=8080, debug=True)