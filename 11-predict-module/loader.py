import os
import time 
from predict_module import PredictModule
import numpy as np
import pandas as pd  
import datetime  
import pytz 

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
            'csv_file': f'''{os.path.dirname(__file__)}/data/bursting-cpu-240628-161624.csv''',   
            'machines_num': 1,   
            'lookback_period': 10,   
            'predict_horizontal': 10,   
            'train_set_percentage': 0.7,   
            'batch_size': 10,   
            'num_epochs': 1000,   
            'learning_rate': 0.01,   
            'input_size': 1,   
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/LSTM_202406281617.pth'''
        self.pm = PredictModule(LSTM, config)

    def train(self):
        return self.pm.train()
   
    def predict(self):
        # Query Prometheus for data
        timestamp = time.time()
        rounded_timestamp = timestamp - (timestamp % 15)
        future_usage = self.pm.predict(self.pth, self.pm.load_data_from_prometheus(rounded_timestamp - 180, rounded_timestamp))
        timestamps = np.arange(rounded_timestamp + 15, rounded_timestamp + 15 * (len(future_usage[0])+1), 15) 
        df = pd.DataFrame(list(zip(timestamps, future_usage[0])), columns=['timestamp', 'data'])  
        local_tz = datetime.datetime.now(pytz.timezone('UTC')).astimezone().tzinfo   
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert(local_tz)  
        print("Predicted future CPU usage:------------------------------")
        print(df)
        return future_usage