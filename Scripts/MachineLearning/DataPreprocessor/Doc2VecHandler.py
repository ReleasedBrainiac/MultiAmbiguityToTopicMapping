
import re
from nltk.corpus import stopwords
from gensim.models.doc2vec import LabeledSentence
from gensim import utils

class Doc2VecHandler(object):
    """
    This pipe is based on https://www.kaggle.com/alyosama/doc2vec-with-keras-0-77
    """

    CLEANUP_REX:str = r"[^A-Za-z0-9^,!.\/'+-=]"
    _stopword_language:str = "german"


    # TODO Missing implementations and workflow updates

    def __init__(self, stopword_language:str = "german", ):
        """
        """
        try:
            pass
        except Exception as ex:
            template = "An exception of type {0} occurred in [Doc2VecHandler.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        

    def CleanSentences(self, sentence:str = None):
        """
        """
        try:
            text = re.sub(self.CLEANUP_REX, " ", text)
            text = text.lower().split()
            stops = set(stopwords.words(self.STOP_WORD_LANGUAGE))
            text = [w for w in text if not w in stops]    
            text = " ".join(text)
            return(text)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Doc2VecHandler.CleanSentences]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GenerateLabeledSentences(self, data:list = None):
        """
        """
        try:
            sentences=[]
            for index, row in data.iteritems():
                sentences.append(LabeledSentence(utils.to_unicode(row).split(), ['Text' + '_%s' % str(index)]))
            return sentences
        except Exception as ex:
            template = "An exception of type {0} occurred in [Doc2VecHandler.GenerateLabeledSentences]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)