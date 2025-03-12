import json
from model.Coordinates import Coordinates
import time
import random

class AGVTelemetryData:

    def __init__(self):
        self.BatteryLevel = 100.0
        self.ON_OFF = "ON"
        self.MissionCoordinates = Coordinates(0.0, 0.0)
        self.timestamp = int(time.time())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def update_measurements(self): #per emulare la generazione di nuovi valori in modo random
        random_x = 0.0 + random.uniform(0.0, 50.0)  #si muove dalla posizione 0.0 alla posizione 50.0
        random_y = 0.0 + random.uniform(0.0, 50.0)

        self.BatteryLevel -= random.uniform(0.0, 100.0) # diminuisce la batteria
        # self.ON_OFF =
        self.MissionCoordinates = Coordinates(random_x, random_y)
        self.timestamp = int(time.time())