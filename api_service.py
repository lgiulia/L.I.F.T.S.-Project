# definizione server HTTP e risorse REST da gestire

from flask import Flask
from flask_restful import Resource, Api, reqparse
from resources.AGVs_resource import AGVsResource
from persistence.data_manager import DataManager
from model.AGV_descriptor import AGVDescriptor
from resources.AGV_resource import AGVResource

app = Flask(__name__)  # crea server flask
api = Api(app)  # crea API tramite FlaskRestFul

ENDPOINT_PREFIX = "/api/iot/inventory"

print("Starting HTTP RESTful API Server ...")

dataManager = DataManager()  # per gestire la memorizzazione dei dati

demoAGV = AGVDescriptor("agv-0001", "KUKA", "alpha.01")

dataManager.add_agv(demoAGV)

api.add_resource(AGVsResource, ENDPOINT_PREFIX + '/AGV',    # aggiunge lista di agvs
                 resource_class_kwargs={'data_manager': dataManager},
                 endpoint="agvs",
                 methods=['GET', 'POST'])

api.add_resource(AGVResource, ENDPOINT_PREFIX + '/AGV/<string:agv_id>',   # aggiunge agv singolo con il suo id
                 resource_class_kwargs={'data_manager': dataManager},
                 endpoint="agv",
                 methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)