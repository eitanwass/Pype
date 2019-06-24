import json

# GPD = Generic Packed Data

class GPD():
    def __init__(self, title, content=None):
        self.title = title
        self.content = content
    

    def to_json(self):
        return json.dumps(self.__dict__)


    @staticmethod
    def rebuild(dict_gpd):
        gpd = GPD('')
        vars(gpd).update(dict_gpd)
        return gpd