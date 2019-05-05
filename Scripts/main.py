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

    def Execute(self):
        """
        The main method of the tool.
        It provides 2 functions:
            1. Storing the cleaned version of the passed AMR file
            2. Execute the network on the given dataset (includes cleaning but no storing of the AMR). 
        """  
        try:
            print("\n#######################################")
            print("######## Graph to Sequence ANN ########")
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


            #inputManager = InputManager()
            #inputManager.runInputRoutin()
            #print(len(inputManager._resultList))

            if not os.path.exists("Basis"):
                os.mkdir("Basis")
            
            reader = Reader("polysem.txt")
            reader_elements=reader.LinesToList()
            for element in reader_elements:
                caller = UniLeipzigAPICaller(element,30)
                caller_list = caller.GetFoundSentences()

                if (len(caller_list) >= 10):
                    print(len(caller_list))
                    open("Basis/"+element+".txt","w+").close()
                    writer = Writer("Basis/"+element+".txt",None, caller_list,None)

            


            #builder = Builder()
            #builder.newEntry()

            #manager = Manager() 


        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteTool]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)
    
if __name__ == "__main__":
    AmbiguityMapper().Execute()