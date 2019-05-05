import os

class Manager():
    MAINPATH = "Dataset/"
    foldername = None

    def __init__(self):
        self.createMainFolder()     

    def createMainFolder(self):
        if not os.path.exists(self.MAINPATH):
            os.mkdir(self.MAINPATH)

    def createFolder(self,name:str):
        try:
            folderpath = self.MAINPATH+name
            if not os.path.exists(folderpath):
                os.mkdir(folderpath)
            self.foldername = name
        except OSError:  
            print ("Creation of the directory %s failed" % name)
        else:  
            print ("Successfully created the directory %s " % name)
        
    def createCategorie(self,name:str):
        path = self.MAINPATH+self.foldername+"/"+name
        open(path,"w+").close()

        
    def createAll(self, word:str, categories:str):
        self.createFolder(word)
        self.createCategorie(categories)
