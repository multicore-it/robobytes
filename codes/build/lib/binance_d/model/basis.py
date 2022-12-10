

class Basis:

    def __init__(self):
        self.pair = ""
        self.contractType = ""
        self.futuresPrice = 0.0
        self.indexPrice = 0.0
        self.basis = 0.0
        self.basisRate = 0.0
        self.timestamp = 0
    
    @staticmethod
    def json_parse(json_data):
        result = Basis()
        result.pair = json_data.get_string("pair")
        result.contractType = json_data.get_string("contractType")
        result.futuresPrice = json_data.get_float("futuresPrice")
        result.indexPrice = json_data.get_float("indexPrice")
        result.basis = json_data.get_float("basis")
        result.basisRate = json_data.get_float("basisRate")
        result.timestamp = json_data.get_int("timestamp")

        return result
