from SupportMethods.ContentSupport import isNotNone, CheckAnyListElementSameType

class Category(object):

    def __init__(self, category:str, sentences:list = None):
        """
        This constructor defines a category sample.
            :param category:str: words category
            :param sentences:list: list of example sentences for the category
        """   
        try:
            self._category = category
            self._sentences = sentences
        except Exception as ex:
            template = "An exception of type {0} occurred in [Category.Constrcutor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GetSentences(self):
        """
        This method returns the sentences.
        """   
        try:    
            if isNotNone(self._category) and isNotNone(self._sentences) and CheckAnyListElementSameType(self._sentences, str):
                return self._sentences
            return None
            
        except Exception as ex:
            template = "An exception of type {0} occurred in [Category.GetSentences]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
    
class Word(object):

    def __init__(self, word:str, categories:list = None):
        """
        This constructor defines a word sample.
            :param word:str: word
            :param categories:str: list of word categories
        """   
        try:
            self._word = word
            self._categories = categories
        except Exception as ex:
            template = "An exception of type {0} occurred in [Word.Constrcutor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GetCategories(self):
        """
        This method returns the categories.
        """   
        try:    
            if isNotNone(self._word) and isNotNone(self._categories) and CheckAnyListElementSameType(self._categories, Category):
                return self._categories
            return None
        except Exception as ex:
            template = "An exception of type {0} occurred in [Word.GetCategories]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)