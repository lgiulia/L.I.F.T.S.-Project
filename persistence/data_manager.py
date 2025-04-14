# Per gestire lo storage dei dati (lettura, creazione e modifica)

from model.AGV_descriptor import AGVDescriptor

class DataManager:

    AGV_dictionary = {}

    def add_agv(self, newagv):
        if isinstance(newagv, AGVDescriptor):   # verifica se newDevice è un'istanza della classe AGVDescriptor
            self.AGV_dictionary[newagv.id] = newagv
        else:
            raise TypeError("Error adding new AGV! Only AVGDescriptor are allowed!")

    def update_agv(self, updatedagv):
        if isinstance(updatedagv, AGVDescriptor):
            self.AGV_dictionary[updatedagv.id] = updatedagv
        else:
            raise TypeError("Error updating the AGV! Only AVGDescriptor are allowed!")

    def remove_agv(self, agvID):
        if agvID in self.AGV_dictionary.keys():
            del self.AGV_dictionary[agvID]