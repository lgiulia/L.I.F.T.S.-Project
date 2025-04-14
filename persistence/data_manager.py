# Per gestire lo storage dei dati (lettura, creazione e modifica)

from model.AGV_descriptor import AGVDescriptor

class DataManager:

    device_dictionary = {}

    def add_device(self, newDevice):
        if isinstance(newDevice, AGVDescriptor):   # verifica se newDevice è un'istanza della classe AGVDescriptor
            self.device_dictionary[newDevice.id] = newDevice
        else:
            raise TypeError("Error adding new device! Only AVGDescriptor are allowerd!")

    def update_device(self, updatedDevice):
        if isinstance(updatedDevice, AGVDescriptor):
            self.device_dictionary[updatedDevice.id] = updatedDevice
        else:
            raise TypeError("Error updating the device! Only AVGDescriptor are allowed!")

    def remove_device(self, deviceID):
        if deviceID in self.device_dictionary.keys():
            del self.device_dictionary[deviceID]