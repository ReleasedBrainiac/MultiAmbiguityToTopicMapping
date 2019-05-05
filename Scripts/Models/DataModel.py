from SupportMethods.ContentSupport import isNotNone

class DataModel():

    def __init__(self, word:str = None, category:str = None, sentence:str = None):
        self._word = word if isNotNone(word) else None
        self._category = category if isNotNone(category) else None
        self._sentence = sentence if isNotNone(sentence) else None
