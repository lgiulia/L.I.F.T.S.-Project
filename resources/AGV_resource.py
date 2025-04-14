# accesso alla risorsa di un singolo AGV. Gestisce le rihcieste che arrivano sui path /AGV/<agv_id>

from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource

class AGVResource(Resource):

    def __init__(self, **kwargs):
        self.dataManager = kwargs['data_manager']

    def get(self, agv_id):
        if agv_id in self.dataManager.AGV_dictionary:
            return self.dataManager.AGV_dictionary[agv_id].__dict__, 200
        else:
            return {'error': "AGV Not Found"}, 404