import os
from SupportMethods.ContentSupport import isNotNone

class Manager():
    MAINPATH = None

    def __init__(self, init_path:str = "Dataset/"):
        try:
            self.MAINPATH = init_path if isNotNone(path) else None
            self._foldername = None
            self.CreateInitFolder()     
        except Exception as ex:
            template = "An exception of type {0} occurred in [FolderManager.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def CreateInitFolder(self):
        try:
            if not os.path.exists(self.MAINPATH): os.mkdir(self.MAINPATH)
        except Exception as ex:
            template = "An exception of type {0} occurred in [FolderManager.CreateInitFolder]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def CreateFolder(self, folder_name:str = None):
        try:
            if not os.path.exists(self.MAINPATH): os.mkdir(self.MAINPATH)
        except Exception as ex:
            template = "An exception of type {0} occurred in [FolderManager.CreateInitFolder]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


    def CreateFolder(self,name:str):
        try:
            folderpath = self.MAINPATH+name
            if not os.path.exists(folderpath):
                os.mkdir(folderpath)
            self._foldername = name
        except OSError:
            print ("Creation of the directory %s failed" % name)
        else:  
            print ("Successfully created the directory %s " % name)
        
    def createCategorie(self,name:str):
        path = self.MAINPATH+self._foldername+"/"+name
        open(path,"w+").close()

        
    def createAll(self, word:str, categories:str):
        self.createFolder(word)
        self.createCategorie(categories)
