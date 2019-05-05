from Models.DataModel import DataModel
from SupportMethods.ContentSupport import isNumber,toInt

class InputManager():

    def __init__(self):
        self._resultList = []
        

    def runInputRoutin(self):
        run = True
        while run:
            word=input("Wort:")
            sub_num = toInt(input("Anzahl Sub:"))
            for sub in range(sub_num):
                sub_name = input("Sub:")
                sens = True
                while sens:
                    sens_input = input("Satz???!!!:")
                    data = DataModel(word,sub_name,sens_input)
                    self._resultList.append(data.toString())
                    print(data.toString())
                    check = input("more??(j/n)")
                    if not check == "j":
                        sens = False
            moreWords = input("weiteres Wort?(j/n)")
            if  not moreWords == "j":
                run = False