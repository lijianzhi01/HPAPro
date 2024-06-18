import argparse  
import time
import requests

def get_slo(start_time, threshold = 300):  
    end_time = time.time()

    # number_of_data_points = (end_time - start_time) / step  
    # rate(): This function calculates the per-second average rate of increase of the time series in the range vector.
    params = {    
        'query': f'sum(rate(http_response_time_seconds_bucket{{namespace="demo", le="{threshold}"}}[20m])) / sum(rate(http_response_time_seconds_count{{namespace="demo"}}[20m]))',    
        'start': start_time,    
        'end': end_time,    
        'step': 15,  # define the interval of time (in seconds) between each data point
    }    
  
    response = requests.get('http://localhost:9090/api/v1/query_range', params=params)    
    data = response.json()      
    last_data_point = data['data']['result'][0]['values'][-1]  
    
    return last_data_point  
  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser()  
    parser.add_argument("--start_time", type=str, help="Start time stamp")  
    parser.add_argument("--threshold", type=float, help="The response time threshold for SLA violation")  
    args = parser.parse_args()  
  
    print(get_slo(args.start_time, args.threshold))
