class IndexPriceEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.pair = ""
        self.indexPrice = 0.0

    @staticmethod
    def json_parse(json_data):
        result = IndexPriceEvent()
        result.eventType = json_data.get_string("e")
        result.eventTime = json_data.get_int("E")
        result.pair = json_data.get_string("i")
        result.indexPrice = json_data.get_float("p")
        return result
