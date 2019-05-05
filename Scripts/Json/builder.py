import json
import os

class Builder():

    def __init__(self):
        self.createJson()

    def createJson(self):
        with open("dataset.json","w") as file:
            string =  """{"Dataset": {}}"""
            json_string = json.loads(string)
            json.dump(json_string,file)
            print("create JSON")
    
    def newEntry(self):
        with open('dataset.json', "r") as json_file:
            data = json.load(json_file)
            print(data)
