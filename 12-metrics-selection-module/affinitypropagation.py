import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler  
from sklearn.cluster import AffinityPropagation  
from itertools import cycle
  
def cluster_metrics(metrics_list, metrics_data, time_string, metric_name='cpu'):  
    # Get data for all cpu metrics    
    filter_metrics_data = {}    
  
    if metric_name == 'all':
        for metric, metric_info in metrics_list.items():    
            filter_metrics_data[metric] = metrics_data[metric]  
    else:
        for metric, metric_info in metrics_list.items():    
            if metric_name in metric.lower():    
                filter_metrics_data[metric] = metrics_data[metric]    
  
    # Prepare data for AffinityPropagation clustering    
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
  
    # Apply Affinity Propagation clustering    
    af = AffinityPropagation(preference=-330).fit(timeseries_data)    
    # [1 2 4 6 9] 5 categories
    cluster_centers_indices = af.cluster_centers_indices_  
    # [3 0 1 4 2 3 3 4 4 4]
    labels = af.labels_  
  
    n_clusters_ = len(cluster_centers_indices)  
  
    print('Estimated number of clusters: %d' % n_clusters_)  
  
    # Plot result  
    plt.figure(figsize=(20, 5 * n_clusters_))  # Adjust as needed  
    plt.title('Estimated number of clusters: %d' % n_clusters_)  
  
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')  
    for k, col in zip(range(n_clusters_), colors):  
        class_members = labels == k  
        cluster_center = timeseries_data[cluster_centers_indices[k]]  
        plt.subplot(n_clusters_, 1, k + 1)  
        timeseries_data_np = np.array(timeseries_data)
        for x, t_metric_name in zip(timeseries_data_np[class_members], np.array(metric_names)[class_members]):  
            plt.plot(x, col, label=t_metric_name)
        # plt.plot(cluster_center, 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
        plt.legend()
  
    plt.savefig(f"report/{time_string}/clusters{metric_name}ap.png")  # Save plot to local file  
    # plt.show()  