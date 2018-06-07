import json 

class Line:
    def __init__(self, name, data):
        self.type = 'line'
        self.stack = '总量'
        self.name = name
        self.data = data
    
    def to_json(self):
        return json.dumps(self.__dict__)