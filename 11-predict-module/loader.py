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
            # LSTM-bursting-cpu
            return LSTM001()
        elif model == "BiLSTM001":
            # BiLSTM-bursting-cpu
            return BiLSTM001()
        elif model == "MF-LSTM-Attention001":
            # MF-LSTM-Attention-bursting-cpu
            return MFLSTMAttention001()
        elif model == "LSTM002":
            return LSTM002()
        elif model == "LSTM002CPU":
            return LSTM002CPU()
        elif model == "LSTM002Mem":
            return LSTM002Mem()
        elif model == "LSTM002Metwork":
            return LSTM002Metwork()
        elif model == "MWDN001":
            return MWDN001()
        elif model == "MWDLSTM001":
            return MWDLSTM001()
        elif model == "LSTMGCT":
            return LSTMGCT001()
        elif model == "BILSTMGCT":
            return BiLSTMGCT()
        elif model == "MWDLSTMGCT":
            return MWDLSTM002()
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

from model.bilstm_gct import BiLSTMGCT as rBiLSTMGCT
class BiLSTM001(BaseModel): 
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
        self.pm = PredictModule(rBiLSTMGCT, config)

from model.mwdn001 import mwdn001 as rmwdn001
class MFLSTMAttention001(BaseModel): 
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
        self.pm = PredictModule(rmwdn001, config)

# test RMSE:  0.0695825853134464
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

# test RMSE:  0.4903527467029748
class MWDN001(BaseModel): 
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
        self.pth = f'''{os.path.dirname(__file__)}/pth/mwdn001_202407190206.pth'''
        self.pm = PredictModule(rmwdn001, config)


# test RMSE:  0.46962186304728815
from model.mwdlstm001 import mwdlstm001 as rmwdlstm001
class MWDLSTM001(BaseModel): 
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
        self.pth = f'''{os.path.dirname(__file__)}/pth/mwdlstm001_202407192012.pth'''
        self.pm = PredictModule(rmwdlstm001, config)

class LSTMGCT001(BaseModel): 
    def __init__(self):    
        print(os.path.dirname(__file__))
        config = {
            'csv_file': f'''{os.path.dirname(__file__)}/data/my_cpu_usage_data.csv''',   
            'machines_num': 1,   
            'lookback_period': 10,   
            'predict_horizontal': 10,   
            'train_set_percentage': 0.7,   
            'batch_size': 10,
            'num_epochs': 2000,   
            'learning_rate': 0.01,   
            'input_size': 1,
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/tmp.pth'''
        self.pm = PredictModule(rLSTM001, config)


class BiLSTMGCT(BaseModel): 
    def __init__(self):    
        print(os.path.dirname(__file__))
        config = {
            'csv_file': f'''{os.path.dirname(__file__)}/data/my_cpu_usage_data.csv''',   
            'machines_num': 1,   
            'lookback_period': 10,   
            'predict_horizontal': 10,   
            'train_set_percentage': 0.7,   
            'batch_size': 10,
            'num_epochs': 2000,   
            'learning_rate': 0.01,   
            'input_size': 1,
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/tmp.pth'''
        self.pm = PredictModule(rBiLSTMGCT, config)

class MWDLSTM002(BaseModel): 
    def __init__(self):    
        print(os.path.dirname(__file__))
        config = {
            'csv_file': f'''{os.path.dirname(__file__)}/data/my_cpu_usage_data.csv''',   
            'machines_num': 1,   
            'lookback_period': 10,   
            'predict_horizontal': 10,   
            'train_set_percentage': 0.7,   
            'batch_size': 10,
            'num_epochs': 2000,   
            'learning_rate': 0.01,   
            'input_size': 1,
        }
        self.pth = f'''{os.path.dirname(__file__)}/pth/mwdlstm001_202407192012.pth'''
        self.pm = PredictModule(rmwdlstm001, config)
