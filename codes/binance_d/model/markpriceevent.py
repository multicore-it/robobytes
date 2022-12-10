class MarkPriceEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.markPrice = 0.0
        self.estSettlmentPrice = 0.0

    @staticmethod
    def json_parse(json_data):
        result = MarkPriceEvent()
        result.eventType = json_data.get_string("e")
        result.eventTime = json_data.get_int("E")
        result.symbol = json_data.get_string("s")
        result.markPrice = json_data.get_float("p")
        result.estSettlmentPrice = json_data.get_float("P")
        return result
