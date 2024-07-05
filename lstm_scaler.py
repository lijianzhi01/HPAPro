import sys
import asyncio 
import numpy as np
  
sys.path.insert(1, '11-predict-module')    
from loader import Loader  
from scaling import scale_deployment, scale_deployment_v2

async def main():  
    loader = Loader()  
      
    # Run predict and get_slo every 10 seconds  
    while True: 
        print("****************************************************************************************************************************************") 
        print("****************************************************************************************************************************************") 
        print("**********************************************************Predicting********************************************************************")
        print("****************************************************************************************************************************************")
        print("****************************************************************************************************************************************")
        cpu = loader.pick("LSTM002").predict()  
        # scale_deployment('demo', 'express', np.max(cpu), cpu[0][0]) 
        scale_deployment_v2('demo', 'express', np.max(cpu), cpu[0][0]) 
        await asyncio.sleep(2)  
  
# Run the main function in the asyncio event loop  
asyncio.run(main())  
