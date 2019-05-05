from Scripts.SupportMethods.ContentSupport import isNotNone
class JSONLoader():

    def __init__(self, path:str = None):
        self._json_path = path if isNotNone(path) else None