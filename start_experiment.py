import sys   
import json  
import asyncio  
  
sys.path.insert(1, '10-simulation/static_sim')  
from play_requests import start_play  
  
async def main():  
    with open('exp_config_001.json', 'r') as f:    
        config = json.load(f)  
  
    port = config['port']    
    rps_record = config['rps_record']    
      
    # Run start_play asynchronously  
    asyncio.create_task(start_play(rps_record, port))  
  
asyncio.run(main())  
