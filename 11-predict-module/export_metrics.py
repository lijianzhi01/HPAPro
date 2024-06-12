import torch  
import torch  
import pandas as pd  
import requests  
import time

def load_data_from_prometheus():
    params = {  
        'query': 'sum(rate(container_cpu_usage_seconds_total{container_label_io_kubernetes_pod_namespace="demo"}[30s]))',  
        'start': time.time() - 3600 * 4,  
        'end': time.time(),  
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
    df.to_csv('./data/my_cpu_usage_data.csv', index=False)

load_data_from_prometheus()