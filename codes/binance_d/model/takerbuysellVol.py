

class TakerBuySellVol:

    def __init__(self):
        self.pair = ""
        self.contractType = ""
        self.takerBuyVol = 0.0
        self.takerSellVol = 0.0
        self.takerBuyVolValue = 0.0
        self.takerSellVolValue = 0.0
        self.timestamp = 0
    
    @staticmethod
    def json_parse(json_data):
        result = TakerBuySellVol()
        result.pair = json_data.get_string("pair")
        result.contractType = json_data.get_string("contractType")
        result.takerBuyVol = json_data.get_float("takerBuyVol")
        result.takerSellVol = json_data.get_float("takerSellVol")
        result.takerBuyVolValue = json_data.get_float("takerBuyVolValue")
        result.takerSellVolValue = json_data.get_float("takerSellVolValue")
        result.timestamp = json_data.get_int("timestamp")

        return result
