from enum import Enum
from keras import activations

class Model(object):

    #TODO: Resourcen da noch alles fehlt
    # => https://keras.io/getting-started/functional-api-guide/
    # => https://keras.io/getting-started/sequential-model-guide/

    _model = None

    def __init__(self):
        try:
            return Create()
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def Create(self):
        # create model
        model = Sequential()
        model.add(Dense(8, input_dim=4, activation='relu'))
        model.add(Dense(3, activation='softmax'))
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def Train(self):
        try:
            pass
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.Train]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def ShowResultAccuracy(self):
        try:
            pass
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.ShowResultAccuracy]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def PredictAndVisualize(self):
        try:
            pass
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.PredictAndVisualize]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)