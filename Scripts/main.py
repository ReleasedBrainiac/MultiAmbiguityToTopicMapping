# -*- encoding: utf-8 -*-
import os, sys
import platform as pf
import unicodedata
import time
#import keras
#import tensorflow as tf
#from pattern.de import parse, split

from FolderManager.manager import Manager
from Json.builder import Builder
from Models.DataModel import DataModel
from Json.inputManager import InputManager
from FileManager.FileWriter import Writer
from FileManager.FileReader import Reader
from FileManager.UniLeipzigApiCaller import UniLeipzigAPICaller

class AmbiguityMapper():

    # For pulling raw data samples
    PULL_DATASET:bool = False
    COLLECT_WORD_LIST_PATH:str = "polysem.txt"
    COLLECTING_LIMIT:int = 30
    COLLECT_API_BASE_URL:str = "http://api.corpora.uni-leipzig.de/ws/sentences/"
    COLLECT_CORPUS:str = "deu_news_2012_1M"
    COLLECT_TASK:str = "sentences"
    DATASET_PATH:str = "Dataset/"
    DATASET_RAW_PATH:str = DATASET_PATH + "Basis/"
    DATASET_SINGLE_FILE_TYP = "txt"


    
    def Execute(self):
        """
        The main method of the tool.
        It provides 2 functions:
            1. Storing the cleaned version of the passed AMR file
            2. Execute the network on the given dataset (includes cleaning but no storing of the AMR). 
        """  
        try:
            print("\n#######################################")
            print("######## Ambiguity Mapper ANN ########")
            print("#######################################\n")

            print("~~~~~~~~~~ System Informations ~~~~~~~~")
            print("Used OS:\t\t=> ", pf.system())
            print("Release:\t\t=> ", pf.release())
            print("Version:\t\t=> ", pf.version())
            print("Architecture:\t\t=> ", pf.architecture())
            print("Machine:\t\t=> ", pf.machine())
            print("Platform:\t\t=> ", pf.platform())
            print("CPU:\t\t\t=> ", pf.processor())
            print("Python Version:\t\t=> ", pf.python_version())
           # print("Tensorflow version: \t=> ", tf.__version__)
            #print("Keras version: \t\t=> ", keras.__version__, '\n')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            if self.PULL_DATASET:
                self.ExecuteRawDatasetCollection()
            else:
                self.ExecuteANNProcessing()
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteTool]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)
    
    def ExecuteANNProcessing(self):
        try:
            #TODO: Currently not in use since the pipe and the network are still missing.
            pass

        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteANNProcessing]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def ExecuteRawDatasetCollection(self):
        try:
            if not os.path.exists(self.DATASET_PATH): 
                os.mkdir(self.DATASET_PATH)

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

if __name__ == "__main__":
    AmbiguityMapper().Execute()