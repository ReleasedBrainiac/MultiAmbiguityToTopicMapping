
import re, os
import multiprocessing
from nltk.corpus import stopwords
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
from gensim import utils
from SupportMethods.ContentSupport import hasContent, isNotNone, SetNumberIf

class Doc2VecHandler(object):
    """
    This pipe is based on https://www.kaggle.com/alyosama/doc2vec-with-keras-0-77
    """

    def __init__(self, docs:list, labels:list, stopword_language:str = None, clean_up_rex:str = None, remove_stopwords:bool = True):
        """
        This constructor set the initial values for the Doc2VecHandler.
            :param docs:list: list of documents
            :param labels:list: list of labels for the documents 
            :param stopword_language:str: language for the stopword corpus
            :param clean_up_rex:str: text cleanup regex pattern
        """   
        try:
            self._remove_stopwords = remove_stopwords
            self._cleanup_rex = clean_up_rex if isNotNone(clean_up_rex) else r"[^A-Za-züÜäÄöÖ0-9^'-]"
            self._stopword_language = stopword_language if isNotNone(stopword_language) else "german"

            if hasContent(docs) and hasContent(labels) and (len(docs) == len(labels)):
                self._docs = docs
                self._labels = labels

        except Exception as ex:
            template = "An exception of type {0} occurred in [Doc2VecHandler.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        

    def CleanSentences(self, sentence:str = None):
        """
        This method returns a cleaned sentence.
            :param sentence:str: the sentence to clean
        """   
        try:
            if isNotNone(sentence):
                text:str = re.sub(self._cleanup_rex, " ", sentence)
                text = text.lower().split()
                stops = set(stopwords.words(self._stopword_language))
                text = [w for w in text if not w in stops]    
                return " ".join(text)
            else: 
                print("Empty sentences expelled!")
                return None
        except Exception as ex:
            template = "An exception of type {0} occurred in [Doc2VecHandler.CleanSentences]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GenerateLabeledSentences(self):
        """
        This method returns labeled senteneces like a tagged document.
        """
        try:
            sentences = []
            for index in range(len(self._docs)):
                if self._remove_stopwords:
                    sentences.append(LabeledSentence(utils.to_unicode(self.CleanSentences(self._docs[index])).split(), [str(index)]))
                else:
                    sentences.append(LabeledSentence(utils.to_unicode(self._docs[index]).split(), [str(index)]))

            return sentences
        except Exception as ex:
            template = "An exception of type {0} occurred in [Doc2VecHandler.GenerateLabeledSentences]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


    def GenerateTextModel(  self, 
                            sentences:list,
                            desired_vec_size:int=300,
                            min_occurence:int=1, 
                            max_distance:int=5, 
                            downsample_threshold:float = 1e-4, 
                            noise_words:int = 5, 
                            workers:int = 4, 
                            epochs:int = 5, 
                            seed:int = 1, 
                            d2v_file:str = "docEmbeddings_5_clean.d2v"):
        """
        This method load or create (new) a text model and return it. In case of generting it will also store the model in a file defined by the given path.
        The implementation is partially oriented at the implementation of https://www.kaggle.com/alyosama/doc2vec-with-keras-0-77/output and 
        the documentation is based on the https://radimrehurek.com/gensim/models/doc2vec.html resoruce.

            :param sentences:list: list of gensim.models.doc2vec.LabeledSentence elements.
            :param desired_vec_size:int: Desired dimensionality of the feature vectors.
            :param min_occurence:int: Ignores all words with total frequency lower than this.
            :param max_distance:int: The maximum distance between the current and predicted word within a sentence.
            :param downsample_threshold:float: The threshold for configuring which higher-frequency words are randomly downsampled, useful range is (0, 1e-5).
            :param noise_words:int: If > 0, negative sampling will be used, the int for negative specifies how many “noise words” should be drawn (usually between 5-20). If set to 0, no negative sampling is used.
            :param workers:int: Use these many worker threads to train the model (=faster training with multicore machines).
            :param epochs:int:  Number of iterations (epochs) over the corpus.
            :param seed:int: Seed for the random number generator. 
            :param d2v_file:str: load or store file path. On exist it try to load a Doc2Vex text model with it. Otherwise it stores the new one right there.
        """   
        try:
            text_model=None
            if os.path.isfile(d2v_file):
                text_model = Doc2Vec.load(d2v_file)
            else:
                
                workers = multiprocessing.cpu_count() if workers == -1 else workers

                print("Define D2V Textmodel")
                text_model = Doc2Vec(   vector_size=SetNumberIf(desired_vec_size, 100, 0, False), 
                                        min_count=SetNumberIf(min_occurence, 1, 1, False), 
                                        window=SetNumberIf(max_distance, 1, 1, False), 
                                        sample=SetNumberIf(downsample_threshold, 1e-3, 0, False), 
                                        negative=SetNumberIf(noise_words, 0, 0, False), 
                                        workers=workers, 
                                        epochs=SetNumberIf(epochs, 1, 1, False), 
                                        seed=SetNumberIf(seed, 1, 1, False))
                print("Build D2V Textmodel")
                text_model.build_vocab(sentences)
                print("Train D2V Textmodel")
                text_model.train(sentences, total_examples=text_model.corpus_count, epochs=text_model.iter)
                print("Save D2V Textmodel")
                text_model.save(d2v_file)
            return text_model
        except Exception as ex:
            template = "An exception of type {0} occurred in [Doc2VecHandler.GenerateTextModel]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)