# accesso alla risorsa di un singolo AGV. Gestisce le richieste che arrivano sui path /AGV/<agv_id>

from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource

from model.AGV_descriptor import AGVDescriptor

class AGVResource(Resource):

    def __init__(self, **kwargs):
        self.dataManager = kwargs['data_manager']

    def get(self, agv_id):
        if agv_id in self.dataManager.AGV_dictionary:
            return self.dataManager.AGV_dictionary[agv_id].__dict__, 200
        else:
            return {'error': "AGV Not Found"}, 404

    def put(self, agv_id):
        if agv_id not in self.dataManager.AGV_dictionary:
            return {'error': f"AGV with id '{agv_id}' Not Found"}, 404

        try:
            data = request.get_json(force=True)
            existing_agv = self.dataManager.AGV_dictionary[agv_id]

            # Crea un nuovo AGVDescriptor con i dati aggiornati (mantenendo i valori esistenti se non forniti)
            updated_agv = AGVDescriptor(
                id=agv_id,  # L'ID viene preso dall'URL
                manufacturer=data.get('manufacturer', existing_agv.manufacturer),
                model=data.get('model', existing_agv.model),
                software_ver=data.get('software_ver', existing_agv.software_ver)
            )

            # Aggiorna l'AGV nel DataManager
            self.dataManager.update_agv(updated_agv)

            return '', 204  # Aggiornamento riuscito, nessun body

        except JSONDecodeError:
            return {'error': "Invalid JSON! Check the request"}, 400
        except Exception as e:
            return {'error': f"Internal Server Error: {str(e)}"}, 500

    def delete(self, agv_id):
        if agv_id not in self.dataManager.AGV_dictionary:
            return {'error': f"AGV with id '{agv_id}' Not Found"}, 404

        try:
            self.dataManager.remove_agv(agv_id)
            return '', 204  # agv con id "agv-n" rimosso con successo, nessun body

        except Exception as e:
            return {'error': f"Internal Server Error: {str(e)}"}, 500