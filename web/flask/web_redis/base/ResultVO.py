from flask import jsonify
class ResultVO:
    def __init__(self, code, count, data):
        self.code = code
        self.count = count 
        self.data = data
    
    @staticmethod
    def single(data):
        return ResultVO(0, 1, data).jsonify()
    
    @staticmethod
    def multiple(data):
        return ResultVO(0, len(data), data).jsonify()
        
    @staticmethod
    def fail(code):
        return ResultVO(code, 0, 0).jsonify()
    
    @staticmethod
    def success():
        return ResultVO(0, 0, 0).jsonify()
    
    def jsonify(self):
        return jsonify({"code":self.code, "count":self.count, "data":self.data})