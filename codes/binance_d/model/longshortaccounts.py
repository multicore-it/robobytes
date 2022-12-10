

class LongShortAccounts:

    def __init__(self):
        self.pair = ""
        self.longShortRatio = 0.0  #  long/short account num ratio of top traders
        self.longAccount = 0.0  # long account num ratio of top traders
        self.shortAccount = 0.0  # short account num ratio of top traders 
        self.timestamp = 0
    
    @staticmethod
    def json_parse(json_data):
        result = LongShortAccounts()
        result.pair = json_data.get_string("pair")
        result.longShortRatio = json_data.get_float("longShortRatio")
        result.longAccount = json_data.get_float("longAccount")
        result.shortAccount = json_data.get_float("shortAccount")
        result.timestamp = json_data.get_int("timestamp")

        return result
