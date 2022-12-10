

class OpenInterestStats:

    def __init__(self):
        self.pair = ""
        self.contractType = ""
        self.sumOpenInterest = 0.0  #  total open interest
        self.sumOpenInterestValue = 0.0  # total open interest value
        self.timestamp = 0
    
    @staticmethod
    def json_parse(json_data):
        result = OpenInterestStats()
        result.pair = json_data.get_string("pair")
        result.contractType = json_data.get_string("contractType")
        result.sumOpenInterest = json_data.get_float("sumOpenInterest")
        result.sumOpenInterestValue = json_data.get_float("sumOpenInterestValue")
        result.timestamp = json_data.get_string("timestamp")

        return result
