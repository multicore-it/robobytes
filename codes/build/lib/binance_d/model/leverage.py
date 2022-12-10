class Leverage:

    def __init__(self):
        self.leverage = 0.0
        self.maxQty = 0.0
        self.symbol = ""

    @staticmethod
    def json_parse(json_data):
        result = Leverage()
        result.leverage = json_data.get_float("leverage")
        result.maxQty = json_data.get_float("maxQty")
        result.symbol = json_data.get_string("symbol")
        
        return result