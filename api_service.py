# definizione server HTTP e risorse REST da gestire

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from resources.AGVs_resource import AGVsResource
from persistence.data_manager import DataManager
from model.AGV_descriptor import AGVDescriptor
from resources.AGV_resource import AGVResource
from resources.MqttTelemetryData import MqttTelemetryData
import json

app = Flask(__name__)  # crea server flask
api = Api(app)  # crea API tramite FlaskRestFul

ENDPOINT_PREFIX = "/api/iot/inventory/AGV"

print("Starting HTTP RESTful API Server ...")

dataManager = DataManager()  # per gestire la memorizzazione dei dati
telemetry_data_manager = {}

with open('InfoData.json','r') as file:
    AGVdata = json.load(file)

for agv in AGVdata:
    demoAGV = AGVDescriptor(agv["id"], agv["manufacturer"], agv["model"], agv["software_ver"], agv["telemetry_data"])
    dataManager.add_agv(demoAGV)
    telemetry_data_manager[agv["id"]] = None # Inizializza lo spazio per i dati di telemetria


api.add_resource(AGVsResource, ENDPOINT_PREFIX,    # aggiunge lista di agvs
                 resource_class_kwargs={'data_manager': dataManager},
                 endpoint="agvs",
                 methods=['GET', 'POST'])

api.add_resource(AGVResource, ENDPOINT_PREFIX + '/<string:agv_id>',   # aggiunge agv singolo con il suo id
                 resource_class_kwargs={'data_manager': dataManager},
                 endpoint="agv",
                 methods=['GET', 'PUT', 'DELETE'])

api.add_resource(MqttTelemetryData, ENDPOINT_PREFIX + '/<string:agv_id>/mqtt_data',
                 resource_class_kwargs={'telemetry_data_manager': telemetry_data_manager},
                 endpoint='mqtt_data')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)