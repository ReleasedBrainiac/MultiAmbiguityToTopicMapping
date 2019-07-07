from SupportMethods.ContentSupport import isNotNone, isNone, CheckAnyListElementSameType
from Models.DataModels import Word, Category

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
    
    def GetTaggedTuple(self):
        """
        This method returns the tagged sample tuple if all values not None.
        This is for Doc2Vec machine learning.
        """   
        try:    
            if isNone(self._word) or isNone(self._category) or isNone(self._sentence):
                return None
            else:
                return (self._word + "_" + self._category, self._sentence)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Sample.GetTaggedTuple]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)



class SampleGenerator(object):

    def __init__(self, word:list = None):
        """
        This class constructor collects a list of word models.
            :param word:list=None: 
        """   
        try:
            self._word_samples = word
        except Exception as ex:
            template = "An exception of type {0} occurred in [SampleGenerator.Constrcutor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GenerateDatasetSamples(self):
        """
        This method generates a list of samples out of the word model list.
        """   
        try:
            if CheckAnyListElementSameType(self._word_samples, Word):
                samples:list = []
                for word in self._word_samples:
                    for category in word.GetCategories():
                        for sentence in category.GetSentences():
                            #TODO size of string and amount of minimum datasets please right here!
                            sample = Sample(word=word.GetName(), category=category.GetName(), sentence=sentence)
                            if isNotNone(sample): samples.append(sample)
                return samples 
            else:
                return None
        except Exception as ex:
            template = "An exception of type {0} occurred in [SampleGenerator.GenerateDatasetSamples]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GenerateTuples(self):
        """
        This method generates 3 element tuples from the collected samples.
        """
        try:
            return [v.GetTuple() for v in  self.GenerateDatasetSamples()]
        except Exception as ex:
            template = "An exception of type {0} occurred in [SampleGenerator.GenerateTuples]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GenerateTaggedTuples(self):
        """
        This method generates 2 element tagged tuples from the collected samples.
        The word and category dimension were merged together.
        """
        try:
            return [v.GetTaggedTuple() for v in  self.GenerateDatasetSamples()]
        except Exception as ex:
            template = "An exception of type {0} occurred in [SampleGenerator.GenerateTaggedTuples]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GenerateLabelsAndDocs(self, samples:list = None):
        """
        This function generates 2 lists from 2D tuple list. [Docs, Labels]
        """
        try:
            if len(samples[0]) >= 2 and len(samples[0]) < 4:
                return zip(*samples)
            else:
                return None
        except Exception as ex:
            template = "An exception of type {0} occurred in [SampleGenerator.GenerateLabelsAndDocs]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

