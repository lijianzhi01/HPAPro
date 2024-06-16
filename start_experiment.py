import sys 
import json

sys.path.insert(1, '11-predict-module')  

from loader import Loader

with open('exp_config_001.json', 'r') as f:  
    config = json.load(f)

port = config['port']  
rps_record = config['rps_record']  
duration = config['duration']  
predictor = config['predictor']  

loader = Loader()
loader.pick(predictor).predict()

sys.path.insert(1, '10-simulation/static_sim')
from play_requests import start_play
start_play(rps_record, port)