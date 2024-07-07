import sys
import asyncio 
import numpy as np
  
sys.path.insert(1, '11-predict-module')    
from loader import Loader  
from scaling import scale_deployment, scale_deployment_v2, scale_deployment_v3

async def main():  
    loader = Loader()  
      
    # Run predict and get_slo every 10 seconds  
    while True: 
        print("****************************************************************************************************************************************") 
        print("****************************************************************************************************************************************") 
        print("**********************************************************Predicting********************************************************************")
        print("****************************************************************************************************************************************")
        print("****************************************************************************************************************************************")
        container_cpu_usage_seconds_total = loader.pick("LSTM002").predict()
        container_memory_failures_total = loader.pick("LSTM002").predict()  
        container_network_transmit_packets_total = loader.pick("LSTM002").predict()  
        # scale_deployment('demo', 'express', np.max(cpu), cpu[0][0]) 
        scale_deployment_v3('demo', 'express', np.max(container_cpu_usage_seconds_total), np.max(container_memory_failures_total), np.max(container_network_transmit_packets_total)) 
        await asyncio.sleep(2)  
  
# Run the main function in the asyncio event loop  
asyncio.run(main())  
