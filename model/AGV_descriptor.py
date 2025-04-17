import json
from wsgiref.simple_server import software_version


class AGVDescriptor:

    def __init__(self, id, manufacturer, model, software_ver):
        self.id = id
        self.manufacturer = manufacturer
        self.model = model
        self.software_ver = software_ver

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)