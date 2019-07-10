from SupportMethods.ContentSupport import isNotNone, isIterable, isList
from random import randrange

class Shuffler(object):

    def __init__(self, *args):
        """
        This constructor collect some params and store them.
            :param *args: 
        """   
        try:
            self._content = args if isNotNone(args) else None
        except Exception as ex:
            template = "An exception of type {0} occurred in [Shuffler.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def CheckListListsAreEqualLength(self, list_lists:list):
        try:
            if len(list_lists) > 1 and isIterable(list_lists[0]):
                init_length:int = len(list_lists[0])
                for new_list in list_lists:
                    if init_length != len(new_list):
                        return False
            return True
        except Exception as ex:
            template = "An exception of type {0} occurred in [Shuffler.CheckListListsAreEqualLength]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def GetRandomIndex(self, upper_border:int):
        try:
            return randrange(upper_border)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Shuffler.GetRandomIndex]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def ShuffleMultiList(self):
        try:
            if isIterable(self._content) and self.CheckListListsAreEqualLength(self._content):
                rnd_index = randrange(len(self._content[0]))

                new_lists:list = []
                for index in range(len(self._content[0])):
                    new_lists.append([self._content[0][index][rnd_index]])
                    self._content[0][index].pop(rnd_index)

                while len(self._content[0][0]) > 0:
                    rnd_index = randrange(len(self._content[0][0]))

                    for index in range(len(self._content[0])):
                        new_lists[index].append(self._content[0][index][rnd_index])
                        self._content[0][index].pop(rnd_index)

                return new_lists
        except Exception as ex:
            template = "An exception of type {0} occurred in [Shuffler.ShuffleMultiList]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def clear(self):
        try:
           self._content = None
        except Exception as ex:
            template = "An exception of type {0} occurred in [Shuffler.clear]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)