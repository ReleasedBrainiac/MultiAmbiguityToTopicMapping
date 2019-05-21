import requests
import json
from SupportMethods.ContentSupport import isNotNone, isNotEmptyString, isInt

class UniLeipzigAPICaller():

    def __init__(self, word:str, result_limit:int, base_url:str = "http://api.corpora.uni-leipzig.de/ws/sentences/", corpus:str = "deu_news_2012_1M", task:str = "sentences"):
        """
        The constructor for the ApiCaller.
            :param word:str: desired word
            :param result_limit:int: limit of results
            :param base_url:str: base url of the api providing server
            :param corpus:str=: the desired corpus 
            :param task:str="sentences": the desired task
        """   
        try:
            self._search_word = word if (isNotNone(word) and isNotEmptyString(word)) else None
            self._search_limit = result_limit if (isNotNone(result_limit) and isInt(result_limit)) else 1

            self._base_url = base_url if (isNotNone(base_url) and isNotEmptyString(base_url)) else "http://api.corpora.uni-leipzig.de/ws/sentences/"
            self._corpus = corpus if (isNotNone(corpus) and isNotEmptyString(corpus)) else "deu_news_2012_1M"
            self._task = task if (isNotNone(task) and isNotEmptyString(task)) else "sentences"
            self._search_url_param = "?limit="

            self._search_url = None
        except Exception as ex:
            template = "An exception of type {0} occurred in [UniLeipzigAPICaller.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def UrlBuilder(self):
        """
        This function constructs the url.
        """   
        try:
            if isNotNone(self._search_word):
                self._search_url = self._base_url + self._corpus +"/" + self._task +"/" + self._search_word + self._search_url_param + str(self._search_limit)
        except Exception as ex:
            template = "An exception of type {0} occurred in [UniLeipzigAPICaller.UrlBuilder]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GetRequestJson(self):
        """
        This function returns the json response.
        """   
        try:
            self.UrlBuilder()
            if isNotNone(self._search_url):
                response = requests.get(self._search_url)

                if response.status_code is 200:
                    json_content = json.loads(response.content)

                    if json_content["count"] > 0:
                        return json_content
                else:
                    if (input("Request failed on ["+self._search_word+"]! Retry? (j/n)") is "j"): 
                        self.GetRequestJson()

            return None
        except Exception as ex:
            template = "An exception of type {0} occurred in [UniLeipzigAPICaller.GetRequestJson]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GetFoundSentences(self):
        """
        This function returns the sentences from get response.
        """   
        try:    
            if (self._task is "sentences"):
                sentences_list = []
                json = self.GetRequestJson()
                if isNotNone(json):
                    for sentence_obj in json['sentences']: 
                        sentences_list.append(sentence_obj['sentence'])
                    return sentences_list
                else:
                    return None
        except Exception as ex:
            template = "An exception of type {0} occurred in [UniLeipzigAPICaller.GetFoundSentences]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)