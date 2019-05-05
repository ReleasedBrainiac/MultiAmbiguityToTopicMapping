import json
import os
from SupportMethods.ContentSupport import isNotNone

class Builder():

    def __init__(self, path:str = "dataset.json"):
        self._json_path = path if isNotNone(path) else None
        self.createJson()


    def Load(self,):
        with open(self._json_path,"w") as file:
            string =  """{"Dataset": {}}"""
            json_string = json.loads(string)
            json.dump(json_string,file)
            print("create JSON")
    
    def newEntry(self):
        with open('dataset.json', "r") as file:
            data = json.load(file)
            print(data)
