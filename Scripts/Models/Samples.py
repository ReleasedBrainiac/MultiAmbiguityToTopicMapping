from SupportMethods.ContentSupport import isNotNone, isNone, CheckAnyListElementSameType
from Scripts.Models.DataModels import Word, Category

class Sample(object):

    def __init__(self, word:str, category:str, sentence:str):
        """
        This class is a model for a single sample containing a word, a category and a example sentence for it.
            :param word:str: word
            :param category:str: word category 
            :param sentence:str: example sentence for the categorized word
        """   
        try:    
            self._word = word if isNotNone(word) else None
            self._category = category if isNotNone(category) else None
            self._sentence = sentence if isNotNone(sentence) else None
        except Exception as ex:
            template = "An exception of type {0} occurred in [Sample.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
        
    def GetTuple(self):
        """
        This method returns the sample tuple if all values not None.
        """   
        try:    
            if isNone(self._word) or isNone(self._category) or isNone(self._sentence):
                return None
            else:
                return (self._word, self._category, self._sentence)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Sample.GetTuple]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

class SampleGenerator(object):

    def __init__(self, word:list = None):
        try:
            self._word_samples = word
        except Exception as ex:
            template = "An exception of type {0} occurred in [SampleGenerator.Constrcutor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GenerateDatasetSamples(self):
        try:
            if CheckAnyListElementSameType(self._word_samples, Word):
                samples:list = []
                for word in self._word_samples:
                    for category in word.GetCategories():
                        for sentence in category.GetSentences():
                            sample = Sample(word=word, category=category, sentence=sentence)
                            if isNotNone(sample): samples.append(sample)
                return samples 
            else:
                return None
        except Exception as ex:
            template = "An exception of type {0} occurred in [SampleGenerator.GenerateDatasetSamples]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

