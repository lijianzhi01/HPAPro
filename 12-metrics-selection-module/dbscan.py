import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN  
from sklearn.preprocessing import MinMaxScaler  
from itertools import cycle
  
def cluster_metrics(metrics_list, metrics_data, time_string, metric_name='cpu', eps=0.3, min_samples=2):  
    # Get data for all cpu metrics    
    filter_metrics_data = {}    
  
    if metric_name == 'all':
        for metric, metric_info in metrics_list.items():    
            filter_metrics_data[metric] = metrics_data[metric]  
    else:
        for metric, metric_info in metrics_list.items():    
            if metric_name in metric.lower():    
                filter_metrics_data[metric] = metrics_data[metric]    
    filter_metrics_data["rps"] = metrics_data["rps"]    
  
    # Prepare data for DBSCAN clustering    
    timeseries_data = []    
    original_timeseries_data = []  # to store original data  
    metric_names = []  # to store metric names  
    for metric, data in filter_metrics_data.items():    
        if data['data']['result']:    
            values = [float(x[1]) for x in data['data']['result'][0]['values']]    
            original_timeseries_data.append(values)  # store original data   
            values_scaled = MinMaxScaler(feature_range=(0, 100)).fit_transform(np.array(values).reshape(-1, 1))
            timeseries_data.append(values_scaled.flatten())   
            metric_names.append(metric)  # store metric name  
    timeseries_data_np = np.array(timeseries_data)   
  
    # Apply DBSCAN clustering    
    db = DBSCAN(eps=180, min_samples=1).fit(timeseries_data)    
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)  
    core_samples_mask[db.core_sample_indices_] = True  
    labels = db.labels_    
  
    # Number of clusters in labels, ignoring noise if present.  
    n_clusters_ = len(set(labels))
    print(f'Estimated number of clusters: {n_clusters_}')  
  
    # Plot result  
    # Black removed and is used for noise instead.  
    plt.figure(figsize=(20, 5 * n_clusters_))  # Adjust as needed  
    plt.title('Estimated number of clusters: %d' % n_clusters_)  
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')  
    for k, col in zip(range(n_clusters_), colors):  
        class_members = labels == k
        cluster_center = timeseries_data[k]  
        plt.subplot(n_clusters_, 1, k + 1)  
        for x, t_metric_name in zip(timeseries_data_np[class_members], np.array(metric_names)[class_members]):  
            plt.plot(x, col, label=t_metric_name)
        # plt.plot(cluster_center, 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
        plt.legend()
  
    plt.title('Estimated number of clusters: %d' % n_clusters_)  
    plt.savefig(f"report/{time_string}/clusters{metric_name}dbs.png")  # Save plot to local file  
    # plt.show()  
