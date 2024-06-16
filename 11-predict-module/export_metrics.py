import argparse  
import torch    
import pandas as pd    
import requests    
from datetime import datetime  
  
def load_data_from_prometheus(start_time_str, end_time_str, pattern):  
    start_time = datetime.strptime(start_time_str, "%Y%m%d%H%M%S").timestamp()  
    end_time = datetime.strptime(end_time_str, "%Y%m%d%H%M%S").timestamp()  
  
    params = {    
        'query': 'sum(rate(container_cpu_usage_seconds_total{container_label_io_kubernetes_pod_namespace="demo"}[30s]))',    
        'start': start_time,    
        'end': end_time,    
        'step': 15,  # define the interval of time (in seconds) between each data point  
    }    
  
    response = requests.get('http://localhost:9090/api/v1/query_range', params=params)    
    data = response.json()    
    values = data['data']['result'][0]['values']  
    df = pd.DataFrame(values, columns=['start_time', 'metric_value'])  
    df['start_time'] = pd.to_datetime(df['start_time'], unit='s')    
    df['start_time'] = df['start_time'].astype(str).str.slice(0, 19)  
    df['machine_id'] = 1  
    df['metric_value'] = torch.FloatTensor(df['metric_value'].values.astype(float))  
    df = df[['start_time', 'machine_id', 'metric_value']]    
    # Drop the timestamp column    
    file_name = "./data/{}-cpu-{}.csv".format(pattern, datetime.now().strftime('%y%m%d-%H%M%S'))  
    df.to_csv(file_name, index=False)  
  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser()  
    parser.add_argument("--start_time", type=str, help="Start time in the format YYYYMMDDHHMMSS")  
    parser.add_argument("--end_time", type=str, help="End time in the format YYYYMMDDHHMMSS")  
    parser.add_argument("--pattern", type=str, help="Pattern for the output file name")  
    args = parser.parse_args()  
  
    load_data_from_prometheus(args.start_time, args.end_time, args.pattern)  
