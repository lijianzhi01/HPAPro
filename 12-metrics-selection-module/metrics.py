import requests    
import os    
import json    
import matplotlib.pyplot as plt
    
# Function to get data for a specific metric    
def fetch_metrics(metric, metric_type, start, end, step):    
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

def load_metrics(start, end):
    # Load metrics from JSON file    
    with open('metrics.json') as f:    
        metrics_json = json.load(f)  

    step = 15   
    # lookback = 3600 * 4  # 4 hours 
    # # lookback = 60 * 20  # 20 minutes
    # now = time.time()    
    # start = ((now - lookback) // step) * step    
    # end = (now // step) * step

    # Get data for all metrics    
    all_metrics_data = {}   
    for metric, metric_info in metrics_json.items():    
        data = fetch_metrics(metric, metric_info[0]["type"], start, end, step)    
        all_metrics_data[metric] = data  

    return metrics_json, all_metrics_data

def save_merics_chart(metrics_data, time_string):
    num_columns = 10  # number of columns for the grid of charts  
    num_metrics = len(metrics_data)  
    num_rows = num_metrics // num_columns if num_metrics % num_columns == 0 else num_metrics // num_columns + 1  
    fig, axs = plt.subplots(num_rows, num_columns, figsize=(num_columns * 5, num_rows * 5))  # 5 is the width and height of each subplot  

    i = 0
    for metric, metric_info in metrics_data.items():    
        # Draw chart for the metric    
        if metric_info['data']['result']:    
            values = [float(x[1]) for x in metric_info['data']['result'][0]['values']]    
            timestamps = [float(x[0]) for x in metric_info['data']['result'][0]['values']]    
        else:    
            # If there's no data, plot an empty graph    
            values = []    
            timestamps = []    
        
        row, col = divmod(i, num_columns)  
        ax = axs[row, col]  
        ax.plot(timestamps, values)    
        ax.set_title(metric)  
        i += 1  
  
    # if number of metrics is not a multiple of num_columns, remove the extra subplots  
    if num_metrics % num_columns != 0:  
        for j in range(num_metrics, num_rows * num_columns):  
            fig.delaxes(axs.flatten()[j])  

        # Define the directory  
    dir_name = f'report/{time_string}'  
    
    # Create the directory if it doesn't exist  
    if not os.path.exists(dir_name):  
        os.makedirs(dir_name) 
    
    plt.tight_layout()  
    plt.savefig(f'report/{time_string}/all_charts.png')    
    # plt.show()  