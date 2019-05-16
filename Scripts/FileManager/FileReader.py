from Models.DataModels import Category
from SupportMethods.ContentSupport import isNotNone, isNone, hasContent

class Reader:
    """
    This class provides a FileReader for text files.
    """

    _reader_encoding = 'utf-8'

    def __init__(self, path:str =None):
        """
        The class constructor. 
            :param path:str: path of file with string content
        """   
        try:
            self._path = path  if not (path is None) else None           
        except Exception as ex:
            template = "An exception of type {0} occurred in [FileReader.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def LinesToList(self):
        """
        This function provides a lines to list file reader.
        """
        try:
            look_up_elements = []
            with open(self._path, 'r', encoding=self._reader_encoding) as fileIn:
                for line in fileIn.readlines(): look_up_elements.append(line.replace("\n",""))
            return look_up_elements
        except Exception as ex:
            template = "An exception of type {0} occurred in [FileReader.LinesToList]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def CategoriesReader(self):
        """
        This function provides file to category objects list file reader.
        """
        try:
            collected_sentences:list = []
            category_name:str = None
            categories:list = []

            with open(self._path, 'r', encoding=self._reader_encoding) as fileIn:
                for line in fileIn.readlines(): 
                    line = line.replace("\n","")

                    if "[" in line and "]" in line:
                        if isNotNone(category_name) and hasContent(collected_sentences):
                            categories.append(Category(category_name, collected_sentences))
                            collected_sentences = []
                            category_name = None

                        category_name = line.replace("[","").replace("]","")
                        
                    else:
                        if len(line) > 0: collected_sentences.append(line)

                if isNotNone(category_name) and hasContent(collected_sentences):
                    categories.append(Category(category_name, collected_sentences))

            return categories
        except Exception as ex:
            template = "An exception of type {0} occurred in [FileReader.CategoriesReader]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)