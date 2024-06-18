import sys   
import json  
import time  
import asyncio  
from datetime import datetime  
  
sys.path.insert(1, '11-predict-module')    
from loader import Loader  
  
sys.path.insert(1, '10-simulation/static_sim')  
from play_requests import start_play  
  
sys.path.insert(1, '7-cadvisor')  
from metrics_loader import get_slo  
  
async def main():  
    with open('exp_config_001.json', 'r') as f:    
        config = json.load(f)  
  
    port = config['port']    
    rps_record = config['rps_record']    
    duration = config['duration']    
    predictor = config['predictor'] 
    slo_response_time = config['slo_response_time']    
  
    loader = Loader()  
      
    # Run start_play asynchronously  
    asyncio.create_task(start_play(rps_record, port))  
  
asyncio.run(main())  
