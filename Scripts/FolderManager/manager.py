import os
from SupportMethods.ContentSupport import isNotNone

class FolderManager():
    _main_path = None

    def __init__(self, init_path:str = "Datasets/"):
        """
        This constructor generate the init folder for the dataset if doesnt exist.
            :param init_path:str: the dataset initial path
        """   
        try:
            self._main_path = init_path
            self._foldername = None
            self.CreateDatasetFolder()     
        except Exception as ex:
            template = "An exception of type {0} occurred in [FolderManager.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def CreateDatasetFolder(self,name:str=None):
        """
        This class creates the initial dataset folder on None input or a desired dataset subfolder on given name"
            :param name:str: name of a dataset subfolder
        """   
        try:
            folderpath = self._main_path+name if isNotNone(name) else self._main_path
            self._foldername = None

            if not os.path.exists(folderpath):
                os.mkdir(folderpath)
            
            if os.path.exists():
                 print ("Successfully created the directory %s " % name)
            else:
                print("Failed to create directory %s !" % name)
        except Exception as ex:
            template = "An exception of type {0} occurred in [FolderManager.CreateDatasetFolder]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message) 