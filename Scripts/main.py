import os, sys
import numpy as np
from numpy import array
import platform as pf
import keras
import tensorflow as tf
from time import gmtime, strftime
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

from SupportMethods.Shuffler import Shuffler
from FolderManager.Manager import FolderManager
from Json.Handler import Handler
from FileManager.FileWriter import Writer
from FileManager.FileReader import Reader
from FileManager.UniLeipzigApiCaller import UniLeipzigAPICaller
from Models.Enums import Process
from Models.DataModels import Word
from SupportMethods.ContentSupport import hasContent, isNotNone, SetNumberIf, isNumber, CollectUniqueByOrderOfAppearance
from Models.Samples import SampleGenerator
from MachineLearning.DataPreprocessor.Doc2VecHandler import Doc2VecHandler
from MachineLearning.ArtificialNeuralNetwork.NetworkModel import Model

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
    TEXT_INPUT_DIM:int = 300

    _json_path:str = 'Datasets/Json/20190620_13_49_23 dataset.json'
    _test_data_split:float = 80.0
    _train_size:int = -1
    _test_size:int = -1
    _batches:int = 64
    _use_stopwords:bool = False
    _epochs:int = -1
    _model_name_basic:str = 'Linguistic_MATT_Model'
    _model_folder:str = _model_name_basic+'_'+strftime(FILE_TIME_FORMAT, gmtime()) + "/"
    _model_name:str = _model_folder + _model_name_basic + '_Eps_' + str(_epochs) + '_batches' + str(_batches) + '_UseStops_' + str(_use_stopwords)

    _use_stopwords_list:list = [True, True, True, True, False, False, False, False]
    _epochs_list:list = [50, 100, 150, 200, 50, 100, 150, 200]
 
    '''
    Ressourcen zum Doc2Vec Ansatz

    https://towardsdatascience.com/multi-class-text-classification-with-doc2vec-logistic-regression-9da9947b43f4
    https://github.com/susanli2016/NLP-with-Python/blob/master/Doc2Vec%20Consumer%20Complaint.ipynb
    https://www.kaggle.com/alyosama/doc2vec-with-keras-0-77
    https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/
    https://radimrehurek.com/gensim/models/doc2vec.html
    https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.TaggedDocument
    https://stackoverflow.com/questions/45125798/how-to-use-taggeddocument-in-gensim
    https://stackoverflow.com/questions/50564928/how-to-use-sentence-vectors-from-doc2vec-in-keras-sequntial-model-for-sentence-s    
    https://medium.com/explorations-in-language-and-learning/how-to-obtain-sentence-vectors-2a6d88bd3c8b

    Outstanding Resources
    https://stackoverflow.com/questions/29760935/how-to-get-vector-for-a-sentence-from-the-word2vec-of-tokens-in-sentence

    '''

    def MultiExecute(self):
        """
        This method allow to run multiple different setups after another.
        """
        for run in range(len(self._epochs_list)):
            self._use_stopwords = self._use_stopwords_list[run]
            self._epochs = self._epochs_list[run]
            self._model_folder = self._model_name_basic+'_'+strftime(self.FILE_TIME_FORMAT, gmtime()) + "/"
            self._model_name = self._model_folder + self._model_name_basic + '_Eps_' + str(self._epochs) + '_batches' + str(self._batches) + '_UseStops_' + str(self._use_stopwords)
            self.Execute()

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
            print("Tensorflow version: \t=> ", tf.__version__)
            print("Keras version: \t\t=> ", keras.__version__, '\n')
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
        """
        This method handle the machine learning part.
        """   
        try:
            print("---------- Set Result Folder ----------")
            
            self.MakeFolderIfMissing(folder_path = self._model_folder)
            
            handler:Handler = Handler(self._json_path, self.JSON_NAME)
            words:list = handler.ReadFromJson()

            if not hasContent(words): 
                print("System stopped on missing train data.")
                sys.exit(1)

            tmp_categories = [word.GetCategories() for word in words]
            flat_list = [item for sublist in tmp_categories for item in sublist]
            
            categorie_names = CollectUniqueByOrderOfAppearance([category.GetName() for category in flat_list])
            categories_count = len(categorie_names)
            print("Categories Count: ", categories_count)
            
            tmp_categories = None
            flat_list = None

            print("--------- Preprocess Dataset ----------")
            generator = SampleGenerator(words)
            words, categories, docs = generator.GenerateLabelsAndDocs(generator.GenerateTuples())
            words, categories, docs = Shuffler([list(words), list(categories), list(docs)]).ShuffleMultiList()

            dataset_size = len(docs)
            self._model_name += '_DataSize_' + str(dataset_size)
            self._test_size = self.TestSplitSize(dataset_size, self._test_data_split)
            self._train_size = dataset_size - self._test_size

            print("dataset_size:\t", self._train_size + self._test_size)
            print("train_size:\t", self._train_size)
            print("test_size:\t", self._test_size)

            print("-------- Build Text Model D2V ---------")
            d2v_handler:Doc2VecHandler = Doc2VecHandler(docs=docs, labels=words, remove_stopwords=self._use_stopwords)
            sentences = d2v_handler.GenerateLabeledSentences()
            text_model = d2v_handler.GenerateTextModel(sentences)

            print("------- One Hot Encode Classes --------")
            int_categories = LabelEncoder().fit_transform(array(categorie_names))
            data_to_class = dict(zip(categorie_names, int_categories))
            class_to_data = dict(zip(int_categories, categorie_names))
            encoded_categories = to_categorical([data_to_class[c] for c in categories])
            
            print("-------- One Hot Encode Words ---------")
            int_words = LabelEncoder().fit_transform(array(words))
            encoded_words = to_categorical(int_words)

            print("-------- Create Network Input ---------")
            text_train_arrays = np.zeros((self._train_size, self.TEXT_INPUT_DIM))
            text_test_arrays = np.zeros((self._test_size, self.TEXT_INPUT_DIM))
            print("Text_DIM: ", len(text_model.docvecs[str(0)]))

            for i in range(self._train_size):
                text_train_arrays[i] = text_model.docvecs[str(i)]

            j=0
            for i in range(self._train_size,self._train_size + self._test_size):
                text_test_arrays[j] = text_model.docvecs[str(i)]
                j=j+1

            train_words = encoded_words[:self._train_size]
            test_words = encoded_words[self._train_size:]
            
            if train_words.shape[0] != text_train_arrays.shape[0]:
                print("The shapes of the doc and word arrays do not match in the first dimension!")

            train_x = np.concatenate((train_words, text_train_arrays), axis=1)
            train_y = encoded_categories[:self._train_size]
            test_x = np.concatenate((test_words, text_test_arrays), axis=1)

            print("Train_X Shape: ", train_x.shape)
            print("Train_Y Shape: ", train_y.shape)
            print("Test Shape: ", test_x.shape)

            print("------ Build and Execute Model --------")
            net_model = Model(init_shape=(train_x.shape[1],), model_folder=self._model_folder, categories=categories_count)
            net_model.Create()
            net_model.Compile()
            net_model.PlotSummary(self._model_name)

            history = net_model.Train(train_x=train_x, train_y=train_y, eps=self._epochs, batches=self._batches)
            print(net_model.ShowResultAccuracy(history))
            net_model.PlotResults(history, model_description=self._model_name)

            train_set_words = [words[w] for w in range(self._train_size,self._train_size + self._test_size)]
            train_set_docs = [sentences[s].words for s in range(self._train_size,self._train_size + self._test_size)]

            net_model.PredictAndVisualize(  test_set=test_x, 
                                            categories = None, 
                                            decode_dict = class_to_data,
                                            test_words = train_set_words, 
                                            test_docs = train_set_docs, 
                                            submission_file_name = self._model_folder + "submission_all.csv")
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

    def TestSplitSize(self, dataset_size:int, split_percentage:float):
        """
        This method return a number for the size of desired test samples from dataset by a given percentage.
            :param dataset_size:int: size of the whole datset
            :param split_percentage:float: desired test size percentage from dataset
        """   
        try:
            if isNumber(dataset_size) and isNumber(split_percentage):
                return round((dataset_size * split_percentage)/100.0)
            else:
                return -1
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.SplitData]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

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
    AmbiguityMapper().MultiExecute()