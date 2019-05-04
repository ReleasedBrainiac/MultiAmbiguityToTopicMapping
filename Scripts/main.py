import os, sys
import platform as pf


class AmbiguityMapper():
    TF_CPP_MIN_LOG_LEVEL:str = '2'
    EPOCHS:int = 5
    VERBOSE:int = 1
    BATCH_SIZE:int = 1
    BUILDTYPE:int = 1
    DATASET_NAME:str = 'AMR Bio/amr-release-training-bio.txt' #'Der Kleine Prinz AMR/amr-bank-struct-v1.6-training.txt' 
    fname = DATASET_NAME.split('/')[0]
    DATASET:str = './Datasets/Raw/'+DATASET_NAME
    GLOVE:str = './Datasets/GloVeWordVectors/glove.6B/glove.6B.100d.txt'
    GLOVE_VEC_SIZE:int = 100
    MODEL:str = "graph2seq_model"
    PLOT:str = "plot.png"
    EXTENDER:str = "dc.ouput"
    MAX_LENGTH_DATA:int = -1
    SHOW_FEEDBACK:bool = False
    STORE_STDOUT:bool = False
    SAVE_PLOTS = False
    SAVING_CLEANED_AMR:bool = False
    KEEP_EDGES:bool = True
    GLOVE_OUTPUT_DIM:int = 100
    GLOVE_VOCAB_SIZE:int = 5000
    VALIDATION_SPLIT:float = 0.2
    MIN_NODE_CARDINALITY:int = 7
    MAX_NODE_CARDINALITY:int = 48
    HOP_STEPS:int = 3
    BIDIRECTIONAL_MULT:int = 2
    SHUFFLE_DATASET:bool = True

    def Execute(self):
        """
        The main method of the tool.
        It provides 2 functions:
            1. Storing the cleaned version of the passed AMR file
            2. Execute the network on the given dataset (includes cleaning but no storing of the AMR). 
        """  
        try:
            if (self.STORE_STDOUT): sys.stdout = open(self.fname+' console_report.txt', 'w')

            print("\n#######################################")
            print("######## Graph to Sequence ANN ########")
            print("#######################################\n")

            print("~~~~~~~~~~ System Informations ~~~~~~~~")
            print("Used OS:\t\t=> ", pf.system())
            print("Release:\t\t=> ", pf.release())
            print("Version:\t\t=> ", pf.version())
            print("Architecture:\t\t=> ", pf.architecture())
            print("Machine:\t\t=> ", pf.machine())
            print("Platform:\t\t=> ", pf.platform())
            print("CPU:\t\t\t=> ", pf.processor())
            print("Python Version:\t\t=> ", pf.python_version())
            print("Tensorflow version: \t=> ", tf.__version__)
            print("Keras version: \t\t=> ", keras.__version__, '\n')

            os.environ['TF_CPP_MIN_LOG_LEVEL'] = self.TF_CPP_MIN_LOG_LEVEL

            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteTool]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)



    def SavePyPlotToFile(self, extender:str = None, orientation:str = 'landscape', image_type:str = 'png'):
        """
        This function is a simple wrapper for the PyPlot savefig function with default values.
            :param extender:str: extender for the filename [Default None]
            :param orientation:str: print orientation [Default 'landscape']
            :parama image_type:str: image file type [Default 'png']
        """   
        try:
            if extender is None:
                plt.savefig((self.fname+'_plot.'+image_type), orientation=orientation)
            else: 
                plt.savefig((self.fname+'_'+extender+'.'+image_type), orientation=orientation)
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.SavePyPlotToFile]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print(ex)
    
if __name__ == "__main__":
    AmbiguityMapper().Execute()