from sklearn.preprocessing import StandardScaler  
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth  
  
def cluster_metrics(metrics_list, metrics_data, time_string, metric_name='cpu'):  
    # Get data for all cpu metrics    
    filter_metrics_data = {}    
  
    for metric, metric_info in metrics_list.items():    
        if metric_name in metric.lower():    
            filter_metrics_data[metric] = metrics_data[metric]    
  
    # Prepare data for Mean Shift clustering    
    timeseries_data = []    
    original_timeseries_data = []  # to store original data  
    for metric, data in filter_metrics_data.items():    
        if data['data']['result']:    
            values = [float(x[1]) for x in data['data']['result'][0]['values']]    
            original_timeseries_data.append(values)  # store original data   
            timeseries_data.append(values)    
  
    # Standardize the time series data to have zero mean and unit variance    
    timeseries_data = StandardScaler().fit_transform(timeseries_data)    
      
    # The following bandwidth can be automatically detected using  
    bandwidth = estimate_bandwidth(timeseries_data, quantile=0.7, n_samples=500)  
  
    # Apply Mean Shift clustering    
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)  
    ms.fit(timeseries_data)    
    labels = ms.labels_  
    cluster_centers = ms.cluster_centers_  
  
    labels_unique = np.unique(labels)  
    n_clusters_ = len(labels_unique)  
  
    print("number of estimated clusters : %d" % n_clusters_)  
  
    # Plot result  
    import matplotlib.pyplot as plt  
    from itertools import cycle  
  
    plt.figure(1)  
    plt.clf()  
  
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')  
    for k, col in zip(range(n_clusters_), colors):  
        my_members = labels == k  
        cluster_center = cluster_centers[k]  
        plt.plot(timeseries_data[my_members, 0], timeseries_data[my_members, 1], col + '.')  
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,  
                 markeredgecolor='k', markersize=14)  
    plt.title('Estimated number of clusters: %d' % n_clusters_)  
    # plt.show()  
