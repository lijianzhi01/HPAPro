import os
from predict_module import PredictModule

from model.lstm import LSTM

class Loader:
    def __init__(self):
        self.ok = "yes"

    def pick(self, model):
        if model == "Lstm001":
            return Lstm001()
        else:
            return None

class BaseModel:
    def train(self):
        return "BaseModel"
    
    def predict(self):
        return "BaseModel"
    
class Lstm001(BaseModel): 
    def __init__(self):    
        print(os.path.dirname(__file__))
        config = {  
            'csv_file': f'''{os.path.dirname(__file__)}/data/bursting-cpu-240616-172016.csv''',   
            'machines_num': 1,   
            'lookback_period': 20,   
            'predict_horizontal': 20,   
            'train_set_percentage': 0.8,   
            'batch_size': 10,   
            'num_epochs': 1000,   
            'learning_rate': 0.01,   
            'input_size': 1,   
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/LSTM_202406161741.pth'''
        self.pm = PredictModule(LSTM, config)

    def train(self):
        return self.pm.train()
   
    def predict(self):
        # Query Prometheus for data
        return self.pm.predict(self.pth, self.pm.load_data_from_prometheus())