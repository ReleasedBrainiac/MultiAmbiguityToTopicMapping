import os, sys
import platform as pf
import keras
import tensorflow as tf

from pattern.de import parse, split
from Scripts.FolderManager.manager import Manager
from Scripts.JSONHandler.builder import Builder

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
            print("Tensorflow version: \t=> ", tf.__version__)
            print("Keras version: \t\t=> ", keras.__version__, '\n')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


            builder = Builder()
            builder.createJson()
            builder.newEntry()

            manager = Manager() 
            run = True
            while run:
                word=input("Wort:")
                manager.createFolder(word)
                sub = True
                while sub:
                    subcategorie=input("Sub:")
                    manager.createCategorie(subcategorie)
                    ready = input("Weitere Kategorie? (j/n)")
                    if not ready == "j":
                        sub = False
                moreWords = input("weiteres Wort?(j/n)")
                if  not moreWords == "j":
                    run = False

        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteTool]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)
    
if __name__ == "__main__":
    AmbiguityMapper().Execute()