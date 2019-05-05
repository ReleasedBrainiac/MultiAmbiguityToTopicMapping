import json
import os

class Builder():

    def __init__(self):
        self.createJson()

    def createJson(self):
        with open("dataset.json","w+") as file:
            string =  """{"Dataset": {}}"""
            json_string = json.loads(string)
            json.dump(json_string,file)
            print("create JSON")

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

