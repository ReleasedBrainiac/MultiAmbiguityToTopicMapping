import os, sys
import platform as pf


class AmbiguityMapper():

    def Execute(self):
        """
        The main method of the tool.
        It provides 2 functions:
            1. Storing the cleaned version of the passed AMR file
            2. Execute the network on the given dataset (includes cleaning but no storing of the AMR). 
        """  
        try:
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
            #print("Tensorflow version: \t=> ", tf.__version__)
            #print("Keras version: \t\t=> ", keras.__version__, '\n')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            
        except Exception as ex:
            template = "An exception of type {0} occurred in [Main.ExecuteTool]. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)



    def SavePyPlotToFile(self, extender:str = None, orientation:str = 'landscape', image_type:str = 'png'):
        """
        This function 
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