import json
from model.Coordinates import Coordinates
import time
import random

class AGVTelemetryData:

    def __init__(self):
        self.BatteryLevel = 100.0
        self.ON_OFF = "ON"
        self.MissionCoordinates = Coordinates(4, 1)
        self.timestamp = int(time.time())
        self.Position = Coordinates(0, 0)
        self.MissionStatus = ""  #completed/ongoing/aborted/paused

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

 #   random_x = 0 + random.uniform(0, 14)  # imponiamo una posizione causale della prima missione
 #   random_y = 0 + random.uniform(0, 16)

    def update_measurements(self): #per emulare la generazione di nuovi valori in modo random

        if self.BatteryLevel > 0 and self.ON_OFF == "ON":
            self.BatteryLevel -= random.uniform(0.0, 2.0) # diminuisce la batteria gradualmente, se la batteria non è esaurita
        else:
            self.ON_OFF = "OFF" #la batteria è esaurita e l'agv si spegne

        if random.random() < 0.05:  # il 5% di probabilità di arresto di emergenza
            self.ON_OFF = "EMERGENCY_STOP"
        elif self.ON_OFF == "EMERGENCY_STOP":  # se era in arresto di emergenza prova a riavviare con probabilità 50%
            if random.random() < 0.5:
                self.ON_OFF = "ON"
            else:
                self.ON_OFF = "OFF"
        else:
            if random.random() < 0.9:  # se non è in emergenza, cambia ON_OFF casualmente
                self.ON_OFF = "ON"
            else:
                self.ON_OFF = "OFF"

       # self.MissionCoordinates = Coordinates(0 + random.uniform(0, 14), 0 + random.uniform(0, 16))

        #algoritmo spostamento agv
        random_x = 0 + int(random.uniform(0, 14))
        random_y = 0 + int(random.uniform(0, 16))

        if self.MissionStatus == "completed":
            self.MissionCoordinates = Coordinates(random_x, random_y)

        if self.ON_OFF == "ON":
            if self.MissionCoordinates.x != self.Position.x or self.MissionCoordinates.y != self.Position.y :

                if self.MissionCoordinates.x == self.Position.x :  #se le coordinate x combaciano (siamo sulla stessa colonna) basta modificare solo le y
                    self.MissionStatus = "ongoing"
                    if  self.Position.y < self.MissionCoordinates.y :
                        self.Position.y += 1 #impostiamo la velocità ad 1 così non abbiamo problemi di overstepping dell'agv, nel caso poi cambieremo la velocità ed implementeremo un altra verifica di posizione ad ogni passo
                    elif self.Position.y > self.MissionCoordinates.y :
                        self.Position.y -= 1

                elif self.MissionCoordinates.x != self.Position.x :
                    self.MissionStatus = "ongoing"
                    if self.Position.y != 0 and self.Position.y != 15:
                        if self.MissionCoordinates.y < 8:
                            self.Position.y -= 1
                        elif self.MissionCoordinates.y >= 8:
                            self.Position.y += 1
                    elif self.Position.y == 0 or self.Position.y == 15 :
                        if self.Position.x < self.MissionCoordinates.x:
                            self.Position.x += 1
                        elif self.Position.x > self.MissionCoordinates.x:
                            self.Position.x -= 1

            elif self.MissionCoordinates.x == self.Position.x and self.MissionCoordinates.y == self.Position.y :
                self.MissionStatus = "completed"
                #self.MissionCoordinates = Coordinates(0 + int(random.uniform(0, 14)), 0 + int(random.uniform(0, 16)))
        else:
            self.MissionStatus = "paused"

        self.timestamp = int(time.time())

