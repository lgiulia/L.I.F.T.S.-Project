import json

class Coordinates:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)