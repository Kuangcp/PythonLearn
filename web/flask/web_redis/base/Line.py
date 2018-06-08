import json 

class Line:
    def __init__(self, name, data):
        self.type = 'line'
        self.stack = 'all'
        self.name = name
        self.data = data
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def to_json_self(self):
        return {
            "name" : self.name, 
            "data" : self.data,
            "type" : self.type,
            "stack": self.stack
        }