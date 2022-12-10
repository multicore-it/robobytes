class Bracket:

    def __init__(self):
        self.bracket = 0
        self.initialLeverage = 0
        self.qtyCap = 0.0
        self.qtyFloor = 0.0
        self.maintMarginRatio = 0.0
        
    @staticmethod
    def json_parse(json_data):
        result = Bracket()
        result.bracket = json_data.get_int("bracket")
        result.initialLeverage = json_data.get_int("initialLeverage")
        result.qtyCap = json_data.get_float("qtyCap")
        result.qtyFloor = json_data.get_float("qtyFloor")
        result.maintMarginRatio = json_data.get_float("maintMarginRatio")
        return result

class LeverageBracket:

    def __init__(self):
        self.pair = ""
        self.brackets = list()
    
    @staticmethod
    def json_parse(json_data):
        result = LeverageBracket()
        result.pair = json_data.get_string("pair")

        element_list = list()
        data_list = json_data.get_array("brackets")
        for item in data_list.get_items():
            element = Bracket.json_parse(item)
            element_list.append(element)
        result.brackets = element_list

        return result
