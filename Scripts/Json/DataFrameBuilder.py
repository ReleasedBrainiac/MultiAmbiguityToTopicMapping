

class DataFrameBuilder(object):

    def __init__(self, *args, **kwargs):
        try:
            pass
        except Exception as ex:
            template = "An exception of type {0} occurred in [DataFrameBuilder.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)