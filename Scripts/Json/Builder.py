import json
import os
from SupportMethods.ContentSupport import isNotNone
from Scripts.Models.DataModels import Word, Category

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

    def NewSentences(self, sentences:list):
        sentences_json = {}
        for index_s in range(sentences):
            if isinstance(sentences[index_s], str):
                sentences_json["S_"+index_s+1] = sentences[index_s]
        return sentences_json

    def NewCategories(self, categories:list):
        categories_json = {}
        for category in categories:
            if isinstance(category, Category):
                categories_json[category.GetName()] = self.NewSentences(category.GetSentences())

        return categories_json

    def NewWords(self, words:list):
        word_json = {}
        for word in words:
            if isinstance(word, Word):
                word_json[word.GetName()] = self.NewCategories(word.GetCategories()) 
        return word_json

    def WriteToJson(self, words:dict):
        data = None
        
        with open(self.file_name, "r+") as json_file:
            data = json.load(json_file)

            for word_name, word in words.items():
                if isinstance(word, Word) and isinstance(word_name, str):
                    data[self._json_name] = word 

        with open("dataset.json","w+") as json_file:
            json.dump(data, json_file)





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

