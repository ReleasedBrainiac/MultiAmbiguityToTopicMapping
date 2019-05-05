class Reader:
    """
    This class provides a FileReader for text files.
    """

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
            with open(self._path, 'r', encoding="utf8") as fileIn:
                for line in fileIn.readlines(): look_up_elements.append(line.replace("\n",""))
            return look_up_elements
        except Exception as ex:
            template = "An exception of type {0} occurred in [FileReader.LinesToList]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)