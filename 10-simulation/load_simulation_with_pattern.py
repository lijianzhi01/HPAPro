import sys  
import time  
import math  
import random  
import requests  
from concurrent.futures import ThreadPoolExecutor  
  
def send_request(port):  
    requests.post(f"http://127.0.0.1:{port}/fibonacci", json={"number": 30})  
  
def main(pattern, port):    
    start = time.time()  
    on_duration = 5  # on for 5 seconds  
    off_duration = 10  # off for 10 seconds  
    while True:    
        if pattern == "bursting":    
            # Predictable Bursting Pattern    
            t = time.time() - start    
            x = int(20 * (math.sin(t / 10) + 1) + 5)  
        elif pattern == "variations":    
            # Variations Pattern    
            x = random.randint(5, 45)  
        elif pattern == "onoff":  
            # On  Off Pattern  
            t = time.time() - start  
            if int(t) % (on_duration + off_duration) < on_duration:  
                x = 20  # peak traffic  
            else:  
                x = 0  # no traffic  
        else:    
            print("Unknown pattern. Please specify either 'bursting', 'variations', or 'onoff'.")    
            sys.exit(1)    
    
        print("Sending {} requests...".format(x))    
  
        if x > 0:  
            # Send x requests in parallel    
            with ThreadPoolExecutor(max_workers=x) as executor:    
                executor.map(send_request, [port]*x)    
    
        # Sleep before starting the next round of requests    
        if pattern == "bursting":    
            time.sleep(1)    
        elif pattern == "variations":  
            time.sleep(random.randint(1, 5))  
        elif pattern == "onoff":  
            time.sleep(1)  
  
  
if __name__ == "__main__":  
    if len(sys.argv) != 3:  
        print(f"Usage: {sys.argv[0]} <pattern> <port>")  
        sys.exit(1)  
  
    main(sys.argv[1], sys.argv[2])
