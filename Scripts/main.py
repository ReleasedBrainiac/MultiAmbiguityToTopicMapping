# -*- encoding: utf-8 -*-
import os, sys
import numpy as np
import platform as pf
from time import gmtime, strftime
#import keras
#import tensorflow as tf

from FolderManager.Manager import FolderManager
from Json.Handler import Handler
from FileManager.FileWriter import Writer
from FileManager.FileReader import Reader
from FileManager.UniLeipzigApiCaller import UniLeipzigAPICaller
from Models.Enums import Process
from Models.DataModels import Word
from SupportMethods.ContentSupport import hasContent, isNotNone, SetNumberIf
from Models.Samples import SampleGenerator
from MachineLearning.DataPreprocessor.Doc2VecHandler import Doc2VecHandler

class AmbiguityMapper():

    # For pulling raw data samples
    _process:Process = Process.DATA_TO_NETWORK
    COLLECT_WORD_LIST_PATH:str = "polysem.txt" #"reduced_polysem.txt"
    COLLECTING_LIMIT:int = 1000
    COLLECT_API_BASE_URL:str = "http://api.corpora.uni-leipzig.de/ws/sentences/"
    COLLECT_CORPUS:str = "deu_wikipedia_2010_1M" #"deu_news_2012_1M"
    COLLECT_TASK:str = "sentences"
    DATASET_PATH:str = "Datasets/"
    DATASET_RAW_PATH:str = DATASET_PATH + "ManualGenerated/" #"Basis/"
    DATASET_SINGLE_FILE_TYP:str = "txt"
    JSON_NAME:str = "dataset"
    JSON_SUB_FOLDER:str = DATASET_PATH+"Json/"
    JSON_FILE_EXT:str = ".json"
    FILE_TIME_FORMAT:str = "%Y%m%d_%H_%M_%S "
    CONSOLE_TIME_FORMAT:str = "%d.%m.%Y %H:%M:%S "
    Text_INPUT_DIM:int = 300

    _json_path:str = 'Datasets/Json/20190620_13_49_23 dataset.json'
    test_size:int = 300
    train_size:int = 2901 - test_size
    
    

    '''
    Ressourcen zum Doc2Vec Ansatz

    https://towardsdatascience.com/multi-class-text-classification-with-doc2vec-logistic-regression-9da9947b43f4
    https://github.com/susanli2016/NLP-with-Python/blob/master/Doc2Vec%20Consumer%20Complaint.ipynb
    https://www.kaggle.com/alyosama/doc2vec-with-keras-0-77
    https://radimrehurek.com/gensim/models/doc2vec.html
    https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.TaggedDocument
    https://stackoverflow.com/questions/45125798/how-to-use-taggeddocument-in-gensim
    https://stackoverflow.com/questions/50564928/how-to-use-sentence-vectors-from-doc2vec-in-keras-sequntial-model-for-sentence-s    
    https://medium.com/explorations-in-language-and-learning/how-to-obtain-sentence-vectors-2a6d88bd3c8b

    Outstanding Resources
    https://stackoverflow.com/questions/29760935/how-to-get-vector-for-a-sentence-from-the-word2vec-of-tokens-in-sentence

    '''

    #TODO implement logger maybe the (F)ile(A)nd(C)onsoleLogger of my master examination

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
            print("Execution Time:\t\t=> ", strftime(self.CONSOLE_TIME_FORMAT, gmtime()))
            print("Used OS:\t\t=> ", pf.system())
            print("Release:\t\t=> ", pf.release())
            print("Version:\t\t=> ", pf.version())
            print("Architecture:\t\t=> ", pf.architecture())
            print("Machine:\t\t=> ", pf.machine())
            print("Platform:\t\t=> ", pf.platform())
            print("CPU:\t\t\t=> ", pf.processor())
            print("Python Version:\t\t=> ", pf.python_version())
            print("Encding:\t\t=> ", sys.stdout.encoding or sys.getfilesystemencoding())
            #print("Tensorflow version: \t=> ", tf.__version__)
            #print("Keras version: \t\t=> ", keras.__version__, '\n')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            print("#######################################")
            if self._process is Process.DATA_TO_NETWORK:
                print("######## RUN MACHINE LEARNING #########")
                print("Dataset: ", self._json_path)
                self.ExecuteANNProcessing()
            elif self._process is Process.DATA_TO_JSON:
                print("######### RUN JSON CONVERSION #########")
                self._json_path = self.JSON_SUB_FOLDER + strftime(self.FILE_TIME_FORMAT, gmtime()) + '_' + self.JSON_NAME + self.JSON_FILE_EXT
                print("Dataset: ", self.DATASET_RAW_PATH)
                print("Destination: ", self._json_path)
                self.ExecuteDatasetToJson()
            else:
                print("######## RUN DATA COLLECTION ##########")
                print("Base_Url: ", self.COLLECT_API_BASE_URL)
                print("Destination: ", self.JSON_SUB_FOLDER)

                self.ExecuteRawDatasetCollection()

            print("#######################################")
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteTool]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)
    
    def ExecuteANNProcessing(self):
        try:
            handler:Handler = Handler(self._json_path, self.JSON_NAME)
            words:list = handler.ReadFromJson()

            if not hasContent(words): 
                print("System stopped on missing train data.")
                sys.exit(1)

            
            print("-------- Generate Dataset D2V ---------")
            generator = SampleGenerator(words)
            labels, docs = generator.GenerateLabelsAndDocs(generator.GenerateTaggedTuples())
            print("Docs: ", len(docs))
            print("Labels: ", len(labels))

            print("-------- Build Text Model D2V ---------")
            d2v_handler:Doc2VecHandler = Doc2VecHandler(docs, labels)
            sentences = d2v_handler.GenerateLabeledSentences()
            print(sentences[0])
            text_model = d2v_handler.GenerateTextModel(sentences)

            text_train_arrays = np.zeros((self.train_size, self.Text_INPUT_DIM))
            text_test_arrays = np.zeros((self.test_size, self.Text_INPUT_DIM))

            for i in range(self.train_size):
                text_train_arrays[i] = text_model.docvecs['t_'+str(i)]

            j=0
            for i in range(self.train_size,self.train_size + self.test_size):
                text_test_arrays[j] = text_model.docvecs['t_'+str(i)]
                j=j+1
    
            print(text_train_arrays[0][:50])


            #TODO: Currently not in use since the pipe and the network are still missing.

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
            handler:Handler = Handler(self._json_path, self.JSON_NAME)
            words:list = []

            for file_item in os.listdir(self.DATASET_RAW_PATH):
                composite_path:str = self.DATASET_RAW_PATH + file_item
                if os.path.exists(composite_path) and os.path.isfile(composite_path): 
                    print(composite_path)
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
            self.SentencesForWordsAPICollector(Reader(self.COLLECT_WORD_LIST_PATH).LinesToList(), self.COLLECTING_LIMIT)
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
                if isNotNone(word_sentences_results) and (len(word_sentences_results) >= min_count):
                    composite_path = self.DATASET_RAW_PATH + word + "." + self.DATASET_SINGLE_FILE_TYP
                    open(composite_path, "w+").close()
                    Writer( input_path=composite_path, 
                            in_elements=word_sentences_results, 
                            in_context=None)
                else:
                    if isNotNone(word_sentences_results):
                        print("Word [",word,"] had ", len(word_sentences_results), "results!")
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