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
        random_x = 0.0 + random.uniform(0.0, 50.0)  #si muove dalla posizione 0.0 alla posizione 50.0, troppo veloce? considera coordx max =14, coordy max=16
        random_y = 0.0 + random.uniform(0.0, 50.0)

        if self.BatteryLevel > 0 and self.ON_OFF == "ON":
            self.BatteryLevel -= random.uniform(0.0, 2.0) # diminuisce la batteria gradualmente, se la batteria non è esaurita
        else:
            self.ON_OFF = "OFF" #la batteria è esaurita e l'agv si spegne

        # self.ON_OFF = bisognerebbe creare una funzione che controlla lo stato dell'agv e dice all'agv se essere acceso/spento/arrestato x motivi di sicurezza
        if random.random() < 0.2:  # il 20% di probabilità di arresto diemergenza
            self.ON_OFF = "EMERGENCY_STOP"
        elif self.ON_OFF == "EMERGENCY_STOP":  # se era in arresto di emergenza prova a riavviare con probabilità 50%
            if random.random() < 0.5:
                self.ON_OFF = "ON"
            else:
                self.ON_OFF = "OFF"
        else:
            if random.random() < 0.5:  # se non è in emergenza, cambia ON_OFF casualmente
                self.ON_OFF = "ON"
            else:
                self.ON_OFF = "OFF"

        self.MissionCoordinates = Coordinates(random_x, random_y)
        self.timestamp = int(time.time())