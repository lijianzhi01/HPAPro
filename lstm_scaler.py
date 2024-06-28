import sys
import asyncio 
import numpy as np
  
sys.path.insert(1, '11-predict-module')    
from loader import Loader  
from scaling import scale_deployment

async def main():  
    loader = Loader()  
      
    # Run predict and get_slo every 10 seconds  
    while True: 
        print("****************************************************************************************************************************************") 
        print("****************************************************************************************************************************************") 
        print("**********************************************************Predicting********************************************************************")
        print("****************************************************************************************************************************************")
        print("****************************************************************************************************************************************")
        cpu = loader.pick("Lstm001").predict()  
        scale_deployment('demo', 'express', np.max(cpu)) 
        await asyncio.sleep(2)  
  
# Run the main function in the asyncio event loop  
asyncio.run(main())  
