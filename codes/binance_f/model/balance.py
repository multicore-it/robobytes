class Balance:

    def __init__(self):
        self.asset = ""
        self.accountAlias = ""
        self.balance = 0.0
        self.availableBalance = 0.0

    @staticmethod
    def json_parse(json_data):
        result = Balance()
        result.asset = json_data.get_string("asset")
        result.accountAlias = json_data.get_string("accountAlias")
        result.balance = json_data.get_float("balance")
        result.availableBalance = json_data.get_float("availableBalance")

        return result