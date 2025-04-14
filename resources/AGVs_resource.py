# accesso alla lista di AGV

from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource, reqparse
from model.AGV_descriptor import AGVDescriptor

class AGVsResource(Resource):

    def __init__(self, **kwargs):   # **kwargs accetta argomenti a parole chiave arbitrarie
        self.dataManager = kwargs['data_manager']  # assegna l'oggetto data_manager all'attributo self.dataManager dell'istanza

    def get(self):  # metodo per gestire le richieste HTTP GET
        agv_list = []
        for agv in self.dataManager.AGV_dictionary.values():
            agv_list.append(agv.__dict__)
        return agv_list, 200   # 200: codice HTTP OK