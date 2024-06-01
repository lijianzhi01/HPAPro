from sklearn.preprocessing import StandardScaler  
import matplotlib.pyplot as plt
import numpy as np
import hdbscan  
  
def cluster_metrics(metrics_list, metrics_data, metric_name='cpu', min_cluster_size=2):  
    # Get data for all cpu metrics    
    filter_metrics_data = {}    
  
    for metric, metric_info in metrics_list.items():    
        if metric_name in metric.lower():    
            filter_metrics_data[metric] = metrics_data[metric]    
  
    # Prepare data for HDBSCAN clustering    
    timeseries_data = []    
    original_timeseries_data = []  # to store original data  
    for metric, data in filter_metrics_data.items():    
        if data['data']['result']:    
            values = [float(x[1]) for x in data['data']['result'][0]['values']]    
            original_timeseries_data.append(values)  # store original data   
            timeseries_data.append(values)    
  
    # Standardize the time series data to have zero mean and unit variance    
    timeseries_data = StandardScaler().fit_transform(timeseries_data)    
  
    # Apply HDBSCAN clustering    
    hdb = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size).fit(timeseries_data)    
    labels = hdb.labels_    
  
    # Number of clusters in labels, ignoring noise if present.  
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)  
    n_noise_ = list(labels).count(-1)  
  
    print(f'Estimated number of clusters: {n_clusters_}')  
    print(f'Estimated number of noise points: {n_noise_}')  
  
    # Plot result  
    # Black removed and is used for noise instead.  
    unique_labels = set(labels)  
    colors = [plt.cm.Spectral(each)  
              for each in np.linspace(0, 1, len(unique_labels))]  
    for k, col in zip(unique_labels, colors):  
        if k == -1:  
            # Black used for noise.  
            col = [0, 0, 0, 1]  
  
        class_member_mask = (labels == k)  
  
        xy = timeseries_data[class_member_mask]  
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),  
                 markeredgecolor='k', markersize=14)  
  
    plt.title('Estimated number of clusters: %d' % n_clusters_)  
    # plt.show()  
