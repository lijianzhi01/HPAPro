from model.lstm import LSTM
from predict_module import PredictModule

config = {  
    'csv_file': './data/gcd_cpu_usage_by_machine.csv',   
    'machines_num': 1,   
    'lookback_period': 144,   
    'predict_horizontal': 6,   
    'train_set_percentage': 0.8,   
    'batch_size': 512,   
    'num_epochs': 1000,   
    'learning_rate': 0.01,   
    'input_size': 1,   
    'output_size': 6  
}  

pm = PredictModule(LSTM, config)
# pm.train()
pm.predict("./pth/LSTM_202406110317.pth", pm.generate_test_data())