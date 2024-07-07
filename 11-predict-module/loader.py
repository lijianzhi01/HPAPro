import os
import time 
from predict_module import PredictModule
import numpy as np
import pandas as pd  
import datetime  
import pytz 

class Loader:
    def __init__(self):
        self.ok = "yes"

    def pick(self, model):
        if model == "LSTM001":
            return LSTM001()
        elif model == "LSTM002":
            return LSTM002()
        elif model == "LSTM002CPU":
            return LSTM002CPU()
        elif model == "LSTM002Mem":
            return LSTM002Mem()
        elif model == "LSTM002Metwork":
            return LSTM002Metwork()
        else:
            return None

class BaseModel:
    def train(self):
        return self.pm.train()
    
    def predict(self, metric='container_cpu_usage_seconds_total'):
        # Query Prometheus for data
        timestamp = time.time()
        rounded_timestamp = timestamp - (timestamp % 15)
        future_usage = self.pm.predict(self.pth, self.pm.load_data_from_prometheus(rounded_timestamp - 180, rounded_timestamp, metric))
        timestamps = np.arange(rounded_timestamp + 15, rounded_timestamp + 15 * (len(future_usage[0])+1), 15) 
        df = pd.DataFrame(list(zip(timestamps, future_usage[0])), columns=['timestamp', 'data'])  
        local_tz = datetime.datetime.now(pytz.timezone('UTC')).astimezone().tzinfo   
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert(local_tz)  
        print("Predicted future CPU usage:------------------------------")
        print(df)
        return future_usage
    
from model.lstm001 import LSTM001 as rLSTM001
class LSTM001(BaseModel): 
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
        self.pth = f'''{os.path.dirname(__file__)}/pth/LSTM001_202406282325.pth'''
        self.pm = PredictModule(rLSTM001, config)

from model.lstm002 import LSTM002 as rLSTM002
class LSTM002(BaseModel): 
    def __init__(self):    
        print(os.path.dirname(__file__))
        config = {
            'csv_file': f'''{os.path.dirname(__file__)}/data/bursting-cpu-240628-161624.csv''',   
            'machines_num': 1,   
            'lookback_period': 10,   
            'predict_horizontal': 10,   
            'train_set_percentage': 0.7,   
            'batch_size': 10,   
            'num_epochs': 2000,   
            'learning_rate': 0.01,   
            'input_size': 1,   
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/LSTM002_202406282323.pth'''
        self.pm = PredictModule(rLSTM002, config)

class LSTM002CPU(BaseModel): 
    def __init__(self):    
        print(os.path.dirname(__file__))
        config = {
            'csv_file': f'''{os.path.dirname(__file__)}/data/bursting-container_cpu_usage_seconds_total-240707-201732.csv''',   
            'machines_num': 1,   
            'lookback_period': 10,   
            'predict_horizontal': 10,   
            'train_set_percentage': 0.7,   
            'batch_size': 10,   
            'num_epochs': 2000,   
            'learning_rate': 0.01,   
            'input_size': 1,   
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/LSTM002_202407072019.pth'''
        self.pm = PredictModule(rLSTM002, config)

class LSTM002Mem(BaseModel): 
    def __init__(self):    
        print(os.path.dirname(__file__))
        config = {
            'csv_file': f'''{os.path.dirname(__file__)}/data/bursting-container_memory_failures_total-240707-201744.csv''',   
            'machines_num': 1,   
            'lookback_period': 10,   
            'predict_horizontal': 10,   
            'train_set_percentage': 0.7,   
            'batch_size': 10,   
            'num_epochs': 2000,   
            'learning_rate': 0.01,   
            'input_size': 1,   
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/LSTM002_202407072020.pth'''
        self.pm = PredictModule(rLSTM002, config)

class LSTM002Metwork(BaseModel): 
    def __init__(self):    
        print(os.path.dirname(__file__))
        config = {
            'csv_file': f'''{os.path.dirname(__file__)}/data/bursting-container_network_transmit_packets_total-240707-201750.csv''',   
            'machines_num': 1,   
            'lookback_period': 10,   
            'predict_horizontal': 10,   
            'train_set_percentage': 0.7,   
            'batch_size': 10,   
            'num_epochs': 2000,   
            'learning_rate': 0.01,   
            'input_size': 1,   
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/LSTM002_202407072020.pth'''
        self.pm = PredictModule(rLSTM002, config)
