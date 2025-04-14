from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource, reqparse
from model.AGV_descriptor import AGVDescriptor

class AGVResource(Resource):

    def __init__(self, **kwargs):   # **kwargs accetta argomenti a parole chiave arbitrarie
        self.dataManager = kwargs['data_manager']  # assegna l'oggetto data_manager all'attributo self.dataManager dell'istanza

    def get(self):  # metodo per gestire le richieste HTTP GET
        device_list = []
        for device in self.dataManager.device_dictionary.values():
            device_list.append(device.__dict__)
        return device_list, 200   # 200: codice HTTP OK