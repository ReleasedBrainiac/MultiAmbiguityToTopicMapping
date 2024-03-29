from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import plot_model
from keras.optimizers import SGD
from keras import regularizers
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from SupportMethods.ContentSupport import isNotNone, isNone
from keras.callbacks import History, ReduceLROnPlateau, BaseLogger, EarlyStopping, ModelCheckpoint

class Model(object):
    """
    This class includs all necessary functionalities round about the keras model train, predict, print and so on.
    """
    _model = None
    

    def __init__(self, init_shape:tuple, model_folder:str, categories:int = -1):
        """
        The constructor.
            :param init_shape:tuple: train data input shape
            :param model_folder:str: folder where the model staff should be saved
            :param categories:int: amount of categories
        """   
        try:
            self._init_shape:tuple = init_shape
            self._categories:int = categories
            self._model_folder:str = model_folder if isNotNone(model_folder) else None
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.Constructor]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def NewDense(self, input_shape:tuple=None, output_dim:int = 256, activation:str='relu', kernel_initializer:str='glorot_normal'):
        """
        This method return a predefined Dense layer depending on the inputs.
            :param input_shape:tuple: input shape of the first layer otherwise set None
            :param output_dim:int: output dim of the layer
            :param activation:str: layer activation function
            :param kernel_initializer:str: kernel generation initializer
        """   
        try:
            if input_shape != None:
                return Dense(units=output_dim, input_shape=input_shape, kernel_initializer=kernel_initializer, activation=activation)
            else:
                return Dense(units=output_dim, kernel_initializer=kernel_initializer, activation=activation)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.NewDense]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def Create(self):
        """
        This method constructs the network model.
        """   
        try:
            self._model = Sequential()
            self._model.add(self.NewDense(input_shape=self._init_shape))
            self._model.add(Dropout(0.25))
            self._model.add(self.NewDense())
            self._model.add(Dropout(0.5))
            self._model.add(self.NewDense(output_dim=80))
            self._model.add(self.NewDense(output_dim=self._categories, input_shape=None, activation="softmax"))
            self._model.summary()
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.Create]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def Compile(self, loss_func:str='categorical_crossentropy', metrics:list=['acc']):
        """
        This method compile a model. Additionally the SGD optimizer will be set.
            :param loss_func:str: desired loss function
            :param metrics:list: list of desired metrics
        """   
        try:
            self._model.compile(loss=loss_func, optimizer='adam', metrics=metrics)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.Compile]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def Train(self, train_x, train_y, val_split:float = 0.2, eps:int = 20, batches:int = 64):
        """
        This method executes the model training process.
            :param train_x: train input
            :param train_y: train desired result
            :param val_split:float: validation split of the train set
            :param eps:int: train epochs
            :param batches:int: the dataset batch size
        """   
        try:
            verbose:int = 1
            base_lr = BaseLogger()
            reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.02, patience=5, min_lr=0.000125, verbose=verbose)
            es = EarlyStopping(monitor='val_loss', mode='min', verbose=verbose, patience=75)
            mc = ModelCheckpoint(self._model_folder+'best_model.h5', monitor='val_acc', mode='max', verbose=verbose, save_best_only=True)

            return self._model.fit( train_x, train_y, 
                                    validation_split=val_split, 
                                    epochs=eps, 
                                    batch_size=batches, 
                                    shuffle=True, 
                                    callbacks=[base_lr, reduce_lr, es, mc])
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.Train]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def ShowResultAccuracy(self, history):
        """
        This method show the train acc results.
            :param history: history of the training
        """   
        try:
            return "Training accuracy: %.2f%% / Validation accuracy: %.2f%%" % (100*history.history['acc'][-1], 100*history.history['val_acc'][-1])
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.ShowResultAccuracy]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def ShowResultLoss(self, history):
        """
        This method show the train loss results.
            :param history: history of the training
        """   
        try:
            return 'Training loss: '+ str(history.history['loss'][-1])[:-6] +' / Validation loss: ' + str(history.history['val_loss'][-1])[:-6]
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.ShowResultLoss]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)        

    def PlotResults(self, history, model_description:str, orientation:str = 'landscape', image_type:str = 'png'):
        """
        This method plot acc and loss from history and store it into seperate files.
            :param history: the train history
            :param model_description:str: name of the model
            :param orientation:str: image orientation
            :param image_type:str: image file type
        """   
        try:
            acc_figure = plt.figure(1)
            acc_figure.suptitle('model categorical accuracy', fontsize=14, fontweight='bold')
            plt.title(self.ShowResultAccuracy(history))

            plt.plot(history.history['acc'])
            plt.plot(history.history['val_acc'])
            plt.ylabel('categorical accuracy')
            plt.xlabel('epoch')
            plt.legend(['train', 'valid'], loc='upper left')
            acc_figure.savefig((model_description+'acc_plot.'+image_type), orientation=orientation)
            acc_figure.clf()

            loss_figure = plt.figure(2)
            loss_figure.suptitle('model loss', fontsize=14, fontweight='bold')
            plt.title(self.ShowResultLoss(history))

            plt.plot(history.history['loss'])
            plt.plot(history.history['val_loss'])
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'valid'], loc='upper left')
            loss_figure.savefig((model_description+'loss_plot.'+image_type), orientation=orientation)
            loss_figure.clf()
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.PlotResults]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def PlotSummary(self, file_name:str = None, show_shapes:bool = True):
        """
        This method print the model summary.
            :param file_name:str=None: 
            :param show_shapes:bool=True: 
        """
        try:
            file_name = (file_name + "_ModelGraph.png") if isNotNone(file_name) else "ann__ModelGraph.png"

            plot_model(self._model, to_file=file_name, show_shapes=show_shapes)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.PlotSummary]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def PredictAndVisualize(self, 
                            test_set, 
                            categories:list, 
                            decode_dict:dict, 
                            test_words:list, 
                            test_docs:list, 
                            submission_file_name:str = "submission_all.csv", 
                            isClasses:bool = True):
        """
        This method predict results for a given test set and store it in a csv file.
            :param test_set: predictable input
            :param categories:list: proba lables 
            :param decode_dict:dict: class decoder dicts
            :param test_words:list: prediction words
            :param test_docs:list: predictions docs
            :param submission_file_name:str: name of the prdicted results file
            :param isClasses:bool: predict classes otherwise probability
        """
        try:
            mapped:dict = {}
            predictions = self._model.predict_classes(test_set) if isClasses else self._model.predict_proba(test_set)

            submission_file_name = submission_file_name if isNotNone(submission_file_name) else "submission_all.csv"
            if isNotNone(test_words): mapped['Words'] = test_words
            if isNotNone(test_docs): mapped['Docs'] = test_docs
            if isNotNone(predictions): mapped['PredClasses'] = predictions
            if isNotNone(decode_dict) and isNotNone(predictions): mapped['ClassNames'] = [decode_dict[p] for p in predictions]
            submission = pd.DataFrame(mapped)
            if categories != None: submission.columns = categories
            submission.to_csv(submission_file_name, index=False)
            submission.head()
        except Exception as ex:
            template = "An exception of type {0} occurred in [Model.PredictAndVisualize]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)