import sys   
import json  
import asyncio  
from datetime import datetime
import numpy as np
  
sys.path.insert(1, '11-predict-module')    
from loader import Loader  
  
sys.path.insert(1, '7-cadvisor')  
from metrics_loader import get_slo  
  
async def main():  
    with open('exp_config_001.json', 'r') as f:    
        config = json.load(f)  
  
    predictor = config['predictor'] 
    slo_response_time = config['slo_response_time']    
  
    loader = Loader()  
      
    # Run predict and get_slo every 10 seconds  
    while True:  
        cpu = loader.pick(predictor).predict()  
        last_slo = get_slo(datetime.now().timestamp() - 1200, slo_response_time)  
        print(f'Current SLO: {last_slo} | Predicted Maximum CPU: {np.max(cpu)}')
        await asyncio.sleep(10)  
  
# Run the main function in the asyncio event loop  
asyncio.run(main())  
