from flask import jsonify


class ResultVO:
    def __init__(self, code, count, data):
        self.code = code
        self.count = count
        self.data = data

    @staticmethod
    def single(data):
        return ResultVO(0, 1, data).to_json()

    @staticmethod
    def multiple(data):
        return ResultVO(0, len(data), data).to_json()

    @staticmethod
    def fail(code):
        return ResultVO(code, 0, 0).to_json()

    @staticmethod
    def success():
        return jsonify({"code":0})

    def to_json(self):
        return jsonify({"code": self.code, "count": self.count, "data": self.data})
