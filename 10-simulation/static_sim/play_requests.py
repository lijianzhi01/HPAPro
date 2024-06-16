import sys  
import time  
import os
import requests  
from concurrent.futures import ThreadPoolExecutor  
  
def send_request(port):  
    start_time = time.time()  
    requests.post(f"http://127.0.0.1:{port}/fibonacci", json={"number": 26})  
    end_time = time.time()  
    response_time = end_time - start_time  
    return response_time  
  
def start_play(filename, port):  
    line_number = 0  
    filepath = f'''{os.path.dirname(__file__)}/{filename}'''
    with open(filepath, 'r') as file:  
        for line in file:  
            line_number += 1  
            concurrent_requests = int(float(line.strip()))  
            if concurrent_requests > 0:  
                # Send concurrent_requests requests in parallel  
                with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:  
                    response_times = list(executor.map(send_request, [port]*concurrent_requests))  
                average_response_time = sum(response_times) / len(response_times)  
                print(f"Line {line_number}: {concurrent_requests} requests take average response time: {average_response_time} seconds")  
            # Sleep before starting the next round of requests  
            time.sleep(1)  
  
if __name__ == "__main__":  
    if len(sys.argv) != 3:  
        print(f"Usage: {sys.argv[0]} <filename> <port>")  
        sys.exit(1)  
  
    start_play(sys.argv[1], sys.argv[2])  
