import requests  
import time  
import json  
import matplotlib.pyplot as plt  
import math  
  
step = 15  
  
def round_time_to_nearest_sec(t):    
    # Round the time to the nearest step seconds    
    return (t // step) * step  
  
now = time.time()  
start = round_time_to_nearest_sec(now - 3600 * 4)    
end = round_time_to_nearest_sec(now)    
  
# Load metrics from JSON file  
with open('metrics.json') as f:  
    metrics = json.load(f)  
  
# Function to get data for a specific metric  
def get_metric_data(metric, metric_type):  
    # Define the parameters for the query  
    if metric_type == "counter":  
        query = 'sum(rate({metric}{{container_label_io_kubernetes_pod_namespace="demo"}}[30s]))'.format(metric=metric)  
    elif metric_type == "gauge":  
        query = 'sum({metric}{{container_label_io_kubernetes_pod_namespace="demo"}})'.format(metric=metric)  
    else:  
        raise ValueError("Unsupported metric type: {}".format(metric_type))  
  
    params = {  
        'query': query,    
        'start': start,    
        'end': end,    
        'step': step  # define the interval of time (in seconds) between each data point  
    }  
  
    # Send the GET request to the Prometheus API  
    response = requests.get('http://localhost:9090/api/v1/query_range', params=params)  
    data = response.json()  
  
    return data  
  
# Get data for all metrics  
all_metrics_data = {}  
num_metrics = len(metrics)  
num_cols = 2  
num_rows = math.ceil(num_metrics / num_cols)  
  
fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, num_rows*5))  
  
for i, (metric, metric_info) in enumerate(metrics.items()):  
    data = get_metric_data(metric, metric_info[0]["type"])  
    all_metrics_data[metric] = data  
  
    # Draw chart for the metric  
    if data['data']['result']:  
        values = [float(x[1]) for x in data['data']['result'][0]['values']]  
        timestamps = [float(x[0]) for x in data['data']['result'][0]['values']]  
    else:  
        # If there's no data, plot an empty graph  
        values = []  
        timestamps = []  
  
    row = i // num_cols  
    col = i % num_cols  
    axs[row, col].plot(timestamps, values)  
    axs[row, col].set_title(metric)  
  
fig.tight_layout()  
plt.show()  
  
# Now all_metrics_data contains the data for all metrics  
