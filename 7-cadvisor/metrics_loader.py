import argparse  
import time
import requests
  
def get_sla_violation(start_time, threshold = 0.2):  
    end_time = time.time()

    params = {    
        'query': 'sum by (namespace)(irate(http_response_time_seconds_sum{namespace="demo"}[30s]))',    
        'start': start_time,    
        'end': end_time,    
        'step': 15,  # define the interval of time (in seconds) between each data point
    }    
  
    response = requests.get('http://localhost:9090/api/v1/query_range', params=params)    
    data = response.json()    
    values = data['data']['result'][0]['values']  
    
    # Calculate the total time that the response time was above the threshold  
    violation_time = sum(float(value[1]) for value in values if float(value[1]) > threshold)  
    
    # Calculate the total time that the response time
    total_time = sum(float(value[1]) for value in values) 
    
    # Calculate the SLA violation  
    sla_violation = violation_time / total_time  
    
    return sla_violation  
  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser()  
    parser.add_argument("--start_time", type=str, help="Start time stamp")  
    parser.add_argument("--threshold", type=float, help="The response time threshold for SLA violation")  
    args = parser.parse_args()  
  
    print(get_sla_violation(args.start_time, args.threshold))
