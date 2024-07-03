from datetime import datetime
import argparse  
import requests  
import pandas as pd  
import pytz
  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser()  
    parser.add_argument("--start_time", type=str, help="Start time in the format YYYYMMDDHHMMSS")  
    parser.add_argument("--end_time", type=str, help="End time in the format YYYYMMDDHHMMSS")  
    args = parser.parse_args()  

    start_time = datetime.strptime(args.start_time, "%Y%m%d%H%M%S").timestamp()  
    end_time = datetime.strptime(args.end_time, "%Y%m%d%H%M%S").timestamp()  
    now = datetime.now()  
    
    params = {  
        'query': 'avg(sum(rate(container_cpu_usage_seconds_total{container_label_io_kubernetes_pod_namespace="demo"}[30s])) by (container_label_io_kubernetes_pod_name) / 0.5 * 100)',  
        'start': start_time,
        'end': end_time,
        'step': 15,  # define the interval of time (in seconds) between each data point
    }  

    response = requests.get('http://localhost:9090/api/v1/query_range', params=params)  
    data = response.json()  
    values = data['data']['result'][0]['values']
    df = pd.DataFrame(values, columns=['timestamp', 'ave_cpu_usage'])
    local_tz = datetime.now(pytz.timezone('UTC')).astimezone().tzinfo 
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert(local_tz)
    print(df)
    ave_cpu_usage_mean = df['ave_cpu_usage'].astype(float).mean()  
    print(f"Average CPU Usage: {ave_cpu_usage_mean}")  
