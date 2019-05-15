import json
import os
from SupportMethods.ContentSupport import isNotNone

class Builder():

    def __init__(self, file_name:str, json_name:str):
        """
        This is the json builder constructor which handles initializing th json file if not exist.
            :param file_name:str: file name
            :param json_name:str: json name
        """   
        try:
            self._file_name = file_name  if isNotNone(file_name) else "dataset"
            self._json_name = json_name if isNotNone(json_name) else "Dataset"
            if not os.path.exists(self._file_name): self.InitJson()
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def InitJson(self):
        """
        This method initialize a new json if it not exist depending on the constructor inputs.
        """   
        try:
            with open(self._file_name, "w+") as file:
                init_json = "{\""+self._json_name+"\": {}}"
                json.dump(json.loads(init_json), file)
            except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.InitJson]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


    #TODO: Hier steht noch arbeit an. Beachte laut solid principles nicht zu extrem verschachteln! Eher single responsibility!

    def createEntry(self, dataList:list):
        json_data = None
        with open(self._file_name, "r+") as json_file:
            json_data = json.load(json_file)    
        for data in dataList:
            print(data)
        with open("dataset.json","w+") as json_file:
            json.dump(data, json_file)



    def buildSubcategorie(self, sentences:list):
        subcategorie={}
        for i in range(sentences):
            subcategorie["sens"+i]=sentences[i]
        return subcategorie
        

    def newEntry(self):
        subcategorie ={}
        subcategorie["s1"]="bananananana"
        subcategorie["s2"]="tadaaa"

        categorie ={}
        categorie["subcategorie"]=subcategorie

        wort={}
        wort["wort"]=categorie

        subcategorie ={}
        subcategorie["s1"]="bananananana"
        subcategorie["s2"]="tadaaa"

        categorie ={}
        categorie["subcategorie"]=subcategorie
        categorie["sub2"]=subcategorie

        wort2={}
        wort2["baum"]=categorie

        data = None

        with open('dataset.json', "r+") as json_file:
            data = json.load(json_file)
            data["Dataset"]["baum"]= categorie 
            data["Dataset"]["brine"]=categorie
        with open("dataset.json","w+") as json_file:
            json.dump(data, json_file)

