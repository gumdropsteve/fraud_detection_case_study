"""
This module makes a class ROCGenerator that takes models and data and returns ROC curves
"""


class ROCGenerator():
    
    def __init__(self):
        self.models=[]
        self.data = None
        self.pickles = []
        
    def add_models(self, list_of_models):
        """
        input:
        list_of_models: a list of model objects
        
        output:
        none
        """
        if type(list_of_models) == list:
            self.models += list_of_models
        else:
            print('input mist be a list of models')
        
    def add_pickles(self, list_of_pickles):
        """
        input: list of paths to pickle filenames
        
        output: none
        """
        if type(list_of_pickles) == list:
            self.pickles += list_of_pickles
        else:
            print('input mist be a list of pickle filenames')
            break
            
        #unpickle pickles and put into list of models
        
        list_of_models = self._unpickle(self.pickles)
        
    def _unpickle(self):
        """
        input: None
        output: A list of unpickled models
        """
        pass
    
    def fit(X,y):
        #fit all models
        pass
    
    def plot_ROC(self):
        #Return a plot of all models on an ROC plot
        
    
        
        