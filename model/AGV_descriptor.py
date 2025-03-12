import json

class AGVDescriptor:

    def __init__(self, id, manufacturer, model):
        self.id = id
        self.manufacturer = manufacturer
        self.model = model

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)