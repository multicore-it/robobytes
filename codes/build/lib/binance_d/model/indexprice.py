

class IndexPrice:

    def __init__(self):
        self.pair = ""
        self.indexPrice = 0.0
        self.time = 0
    
    @staticmethod
    def json_parse(json_data):
        result = IndexPrice()
        result.pair = json_data.get_string("pair")
        result.indexPrice = json_data.get_float("indexPrice")
        result.estimatedSettlePrice = json_data.get_float("estimatedSettlePrice")
        result.time = json_data.get_int("time")

        return result
