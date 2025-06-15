import json

class AGVDescriptor:

    def __init__(self, id, manufacturer, model, software_ver, senml=None):
        self.id = id
        self.manufacturer = manufacturer
        self.model = model
        self.software_ver = software_ver
        self.senml = senml

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)