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

    def post(self):
        try:
            json_data = request.get_json(force=True)
            AgvDescriptor = AGVDescriptor(**json_data)
            if AgvDescriptor.id in self.dataManager.AGV_dictionary:
                return {'error': "AGV ID already exists"}, 409
            else:
                self.dataManager.add_agv(AgvDescriptor)
                return Response(status=201, headers={"Location": request.url+"/"+AgvDescriptor.id})
        except JSONDecodeError:
            return {'error': "Invalid JSON! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error! Reason: " + str(e)}, 500