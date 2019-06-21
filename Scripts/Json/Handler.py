import json
import os
from SupportMethods.ContentSupport import isNotNone, hasContent
from Models.DataModels import Word, Category

class Handler():

    _encoding = 'utf-8'

    def __init__(self, file_name:str, json_name:str):
        """
        This is the json builder constructor which handles initializing th json file if not exist.
            :param file_name:str: file name
            :param json_name:str: json name
        """   
        try:
            self._file_name = file_name  if isNotNone(file_name) else "dataset.json"
            self._json_name = json_name if isNotNone(json_name) else "dataset"
            if not os.path.exists(self._file_name): 
                self.InitJson()
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def InitJson(self):
        """
        This method initialize a new json if it not exist depending on the constructor inputs.
        """   
        try:
            with open(self._file_name, "w+", encoding=self._encoding) as file:
                init_json = "{\""+self._json_name+"\": {}}"
                json.dump(json.loads(init_json, encoding=self._encoding), file, ensure_ascii=False)
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.InitJson]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def NewSentences(self, sentences:list):
        """
        This method returns a json applyable dictionairy of sentence entries.
            :param sentences:list: list of sentences
        """   
        try:
            sentences_json = {}
            for index_s in range(len(sentences)):
                if isinstance(sentences[index_s], str):
                    key = "S_"+ str(index_s+1)
                    sentences_json[key] = sentences[index_s]
            return sentences_json
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.NewSentences]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def NewCategories(self, categories:list):
        """
        This method returns a json applyable dictionairy of category object entries.
            :param categories:list: list of category objects
        """   
        try:
            categories_json = {}
            for category in categories:
                if isinstance(category, Category):
                    categories_json[category.GetName()] = self.NewSentences(category.GetSentences())

            return categories_json
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.NewCategories]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def NewWords(self, words:list):
        """
        This method returns a json applyable dictionairy of word object entries. 
            :param words:list: list of word objects
        """
        try:
            word_json = {}
            for word in words:
                if isinstance(word, Word):
                    word_json[word.GetName()] = self.NewCategories(word.GetCategories()) 
            return word_json
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.NewWords]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def WriteToJson(self, words:dict):
        """
        This method writes a json applyable dictionairy of word objects to a json file.
            :param words:dict: dictionairy of word objects
        """
        try:
            data = None
            
            with open(self._file_name, "r+", encoding=self._encoding) as json_file:
                data = json.load(json_file)

                for word_name, word in words.items():
                    if isinstance(word, dict) and isinstance(word_name, str):
                        data[self._json_name][word_name] = word 

            with open(self._file_name,"w+", encoding=self._encoding) as json_file:
                json.dump(data, json_file, ensure_ascii=False)
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.WriteToJson]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def ReadFromJson(self):
        try:
            categories:list = []
            words:list = []
            dataset = None

            with open(self._file_name, "r+", encoding=self._encoding) as json_file:
                dataset = json.load(json_file)[self._json_name]

            for word_name, word in dataset.items():
                for category_name, category in word.items():
                    sentences = [v for v in category. values()]
                    if hasContent(sentences):    
                        categories.append(Category(category_name, sentences))

                if hasContent(categories):
                    words.append(Word(word_name, categories))

            return words
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.ReadFromJson]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GetJsonString(self):
        """
        This method returns the json string of file and json dataset name defined in the constructor.
        """
        try:
            with open(self._file_name, "r+", encoding=self._encoding) as json_file:
                return json.load(json_file)[self._json_name]
        except Exception as ex:
            template = "An exception of type {0} occurred in [JsonBuilder.GetJson]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)