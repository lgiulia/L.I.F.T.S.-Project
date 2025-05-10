from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource

class MqttTelemetryData(Resource):
    def __init__(self, telemetry_data_manager):
        self.telemetry_data_manager = telemetry_data_manager

    def post(self, agv_id):
        try:
            senml_data = request.get_json(force=True)
            print(f"Received SenML data for AGV {agv_id} via HTTP:", senml_data)
            self.telemetry_data_manager[agv_id] = senml_data # Memorizza i dati di telemetria
            return {'message': f'SenML data received and stored for AGV {agv_id}'}, 200
        except Exception as e:
            return {'error': f'Error processing SenML data for AGV {agv_id}: {str(e)}'}, 500

    def get(self, agv_id):
        if agv_id in self.telemetry_data_manager:
            telemetry_data = self.telemetry_data_manager[agv_id]
            if telemetry_data:
                return {'telemetry': telemetry_data}, 200
            else:
                return {'message': f'No telemetry data available for AGV {agv_id} yet'}, 200
        else:
            return {'error': f'AGV with ID {agv_id} not found'}, 404