import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler  
from sklearn.cluster import AffinityPropagation  
from itertools import cycle
  
def cluster_metrics(metrics_list, metrics_data, metric_name='cpu'):  
    # Get data for all cpu metrics    
    filter_metrics_data = {}    
  
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
            timeseries_data.append(values)    
            metric_names.append(metric)  # store metric name  
  
    # Standardize the time series data to have zero mean and unit variance    
    timeseries_data = StandardScaler().fit_transform(timeseries_data)    
  
    # Apply Affinity Propagation clustering    
    af = AffinityPropagation(preference=-50).fit(timeseries_data)    
    cluster_centers_indices = af.cluster_centers_indices_  
    labels = af.labels_  
  
    n_clusters_ = len(cluster_centers_indices)  
  
    print('Estimated number of clusters: %d' % n_clusters_)  
  
    # Plot result  
    plt.figure(figsize=(10, 5 * n_clusters_))  # Adjust as needed  
  
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')  
    for k, col in zip(range(n_clusters_), colors):  
        class_members = labels == k  
        cluster_center = timeseries_data[cluster_centers_indices[k]]  
        plt.subplot(n_clusters_, 1, k + 1)  
        for x, metric_name in zip(timeseries_data[class_members], np.array(metric_names)[class_members]):  
            plt.plot(x, col, label=metric_name)  
        plt.plot(cluster_center, 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)  
        plt.legend()  
  
    plt.title('Estimated number of clusters: %d' % n_clusters_)  
    plt.savefig('clusters.png')  # Save plot to local file  
    # plt.show()  