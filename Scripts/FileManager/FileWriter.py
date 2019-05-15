from SupportMethods.ContentSupport import isStr, isNotNone, isNone
from SupportMethods.ContentSupport import AssertNotNone, isNotEmptyString

class Writer:
    """
    This class provides a Writer to store string or list of string context.
    """
    _writer_encoding = 'utf8'
    _context = None
    _elements = None
    _out_path = None
    

    def __init__(self, input_path:str, file_extender:str = None, in_elements:list = None, in_context:str = None):
        """
        This is the constructor of the Writer class.
            :param input_path:str: path of the input file
            :param file_extender:str: extender to create output file from input path
            :param in_elements:list: amr data pairs list like List<Array{sentence, semantic}>
            :param in_context:str: optional if no data pairs present use context
        """   
        try:
            self._out_path = (input_path+'.'+ file_extender) if isNotEmptyString(file_extender) else input_path
            print('Destination: ', self._out_path)

            if isNotNone(self._out_path):
                if isNotNone(in_elements):
                    self._elements = in_elements
                    self.StoreListElements()

                if isNotNone(in_context):
                    self._context = in_context
                    self.StoreStringContext()

                if(isNone(in_elements) and isNone(in_context)):
                    print("No Input was given for the FileWriter!")
            else:
                print("Given path for FileWriter was None!")

        except Exception as ex:
            template = "An exception of type {0} occurred in [FileWriter.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def StoreStringContext(self):
        """
        This function saves stringified context into a given file.
        """
        try:
            with open(self._out_path, 'w', encoding=self._writer_encoding) as fileOut:
                if isNotNone(self._context) and isStr(self._context):
                    fileOut.write(self._context)
                    fileOut.flush()
        except ValueError:
            print('WRONG INPUT FOR [FileWriter.StoreStringContext]')
        except Exception as ex:
            template = "An exception of type {0} occurred in [FileWriter.StoreStringContext]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def StoreListElements(self):
        """
        This function save a string collection to a given file.
        """
        try:
            with open(self._out_path, 'w', encoding=self._writer_encoding) as fileOut:
                for elem in self._elements:
                    if isNotNone(elem):
                        fileOut.write(elem+"\n")
                        fileOut.flush()
        except ValueError:
            print('WRONG INPUT FOR [FileWriter.StoreListElements]')
        except Exception as ex:
            template = "An exception of type {0} occurred in [FileWriter.StoreListElements]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)