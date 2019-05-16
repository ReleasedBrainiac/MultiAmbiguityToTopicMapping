# -*- encoding: utf-8 -*-
import os, sys
import platform as pf
from time import gmtime, strftime
import keras
import tensorflow as tf

from FolderManager.Manager import FolderManager
from Json.Handler import Handler
from FileManager.FileWriter import Writer
from FileManager.FileReader import Reader
from FileManager.UniLeipzigApiCaller import UniLeipzigAPICaller
from Models.Enums import Process
from Models.DataModels import Word
from SupportMethods.ContentSupport import hasContent
from Models.Samples import SampleGenerator

class AmbiguityMapper():

    # For pulling raw data samples
    _process:Process = Process.DATA_TO_NETWORK
    COLLECT_WORD_LIST_PATH:str = "polysem.txt"
    COLLECTING_LIMIT:int = 30
    COLLECT_API_BASE_URL:str = "http://api.corpora.uni-leipzig.de/ws/sentences/"
    COLLECT_CORPUS:str = "deu_news_2012_1M"
    COLLECT_TASK:str = "sentences"
    DATASET_PATH:str = "Datasets/"
    DATASET_RAW_PATH:str = DATASET_PATH + "Basis/"
    DATASET_SINGLE_FILE_TYP = "txt"
    JSON_NAME = "dataset"
    JSON_SUB_FOLDER = DATASET_PATH+"Json/"
    JSON_PATH = JSON_SUB_FOLDER + JSON_NAME + ".json"
    _file_time_format:str = "%Y%m%d %H_%M_%S"
    _console_time_format = "%d.%m.%Y %H:%M:%S"
    _time_now:str = None
    
    def Execute(self):
        """
        The main method of the tool.
        It provides 2 functions:
            1. Storing the cleaned version of the passed AMR file
            2. Execute the network on the given dataset (includes cleaning but no storing of the AMR). 
        """  
        try:
            self._time_now = strftime(self._console_time_format, gmtime())

            print("\n#######################################")
            print("######## Ambiguity Mapper ANN ########")
            print("#######################################\n")

            print("~~~~~~~~~~ System Informations ~~~~~~~~")
            print("Execution Time:\t\t=> ", self._time_now)
            print("Used OS:\t\t=> ", pf.system())
            print("Release:\t\t=> ", pf.release())
            print("Version:\t\t=> ", pf.version())
            print("Architecture:\t\t=> ", pf.architecture())
            print("Machine:\t\t=> ", pf.machine())
            print("Platform:\t\t=> ", pf.platform())
            print("CPU:\t\t\t=> ", pf.processor())
            print("Python Version:\t\t=> ", pf.python_version())
            print("Tensorflow version: \t=> ", tf.__version__)
            print("Keras version: \t\t=> ", keras.__version__, '\n')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            if self._process is Process.DATA_TO_NETWORK:
                self.ExecuteANNProcessing()
            elif self._process is Process.DATA_TO_JSON:
                self.ExecuteDatasetToJson()
            else:
                self.ExecuteRawDatasetCollection()

        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteTool]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)
    
    def ExecuteANNProcessing(self):
        try:
            #TODO: Currently not in use since the pipe and the network are still missing.
            generator:SampleGenerator = None
            handler:Handler = Handler(self.JSON_PATH, self.JSON_NAME)
            words:list = handler.ReadFromJson()

            if not hasContent(words): 
                print("System stopped on missing train data.")
                sys.exit(1)

            generator = SampleGenerator(words)
            samples = [v.GetTuple() for v in  generator.GenerateDatasetSamples()]
            


        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteANNProcessing]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)
    
    def ExecuteDatasetToJson(self):
        """
        This method allow to store the dataset as preprocessed json structure.
        """   
        try:
            self.MakeFolderIfMissing(self.JSON_SUB_FOLDER)
            handler:Handler = Handler(self.JSON_PATH, self.JSON_NAME)
            words:list = []

            for file_item in os.listdir(self.DATASET_PATH):
                composite_path:str = self.DATASET_PATH + file_item
                if os.path.exists(composite_path) and os.path.isfile(composite_path): 
                    words.append(Word(file_item.replace(".txt","").lower(), Reader(composite_path).CategoriesReader()))
            
            handler.WriteToJson(handler.NewWords(words))
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteDatasetToJson]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)

    def ExecuteRawDatasetCollection(self):
        try:
            self.MakeFolderIfMissing(self.DATASET_PATH)
            self.SentencesForWordsAPICollector(Reader(self.COLLECT_WORD_LIST_PATH).LinesToList())
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteRawDatasetCollection]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def SentencesForWordsAPICollector(self, words:list, min_count:int = 10):
        """
        This function collects sentences for list of words from given API 
        and store them in a local folder as raw dataset elements in text files!
            :param words:list: list of words where sentences have to be collected for
            :param min_count:int: the minimal amount of sentences to get by calling the API less results will expell the word
        """   
        try:
            if not os.path.exists(self.DATASET_RAW_PATH): os.mkdir(self.DATASET_RAW_PATH)

            for word in words:
                word_sentences_results = UniLeipzigAPICaller(   word, 
                                                                self.COLLECTING_LIMIT,
                                                                self.COLLECT_API_BASE_URL,
                                                                self.COLLECT_CORPUS,
                                                                self.COLLECT_TASK).GetFoundSentences()
                if (len(word_sentences_results) >= min_count):
                    composite_path = self.DATASET_RAW_PATH + word + "." + self.DATASET_SINGLE_FILE_TYP
                    open(composite_path, "w+").close()
                    writer = Writer(input_path=composite_path, 
                                    in_elements=word_sentences_results, 
                                    in_context=None)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.SentencesForWordsAPICollector]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)

    def MakeFolderIfMissing(self, folder_path:str):
        """
        This method creates a missing folder.
            :param folder_path:str: 
        """   
        try:
            if not os.path.exists(folder_path): 
                os.mkdir(folder_path)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.MakeFolderIfMissing]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

if __name__ == "__main__":
    AmbiguityMapper().Execute()