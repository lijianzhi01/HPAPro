# pip install tslearn  
import matplotlib.pyplot as plt
import numpy as np
from tslearn.clustering import KShape  
from tslearn.preprocessing import TimeSeriesScalerMeanVariance  

def cluster_cpu_metrics(metrics_list, metrics_data):
    # Get data for all cpu metrics  
    cpu_metrics_data = {}  
    
    for metric, metric_info in metrics_list.items():  
        if 'cpu' in metric.lower():  
            cpu_metrics_data[metric] = metrics_data[metric]  
    
    # Prepare data for KShape clustering  
    timeseries_data = []  
    original_timeseries_data = []  # to store original data
    for metric, data in cpu_metrics_data.items():  
        if data['data']['result']:  
            values = [float(x[1]) for x in data['data']['result'][0]['values']]  
            original_timeseries_data.append(values)  # store original data 
            timeseries_data.append(values)  
    
    # Rescale the time series data to have zero mean and unit variance  
    timeseries_data = TimeSeriesScalerMeanVariance().fit_transform(timeseries_data)  
    
    # Apply KShape clustering  
    n_clusters = 3  # number of clusters  
    ks = KShape(n_clusters=n_clusters, n_init=50, verbose=True)  
    y_pred = ks.fit_predict(timeseries_data)  
    
    # Plot the clustered time series data  
    fig, axs = plt.subplots(n_clusters, 2, figsize=(10, n_clusters * 5))  
    # If there's only one row of subplots, convert axs to a 2D array  
    if n_clusters == 1:  
        axs = np.array([axs]).reshape(1, -1)
    for yi in range(n_clusters):  
        for xx in timeseries_data[y_pred == yi]:  
            axs[yi].plot(xx.ravel(), "k-", alpha=.2)  

        for xx in original_timeseries_data:  # plot original data in second column  
            axs[yi][1].plot(xx, "k-", alpha=.2)  # plot original data  

        axs[yi][0].plot(ks.cluster_centers_[yi].ravel(), "r-")  
        axs[yi][0].set_title("Cluster %d" % (yi + 1))  
        axs[yi][1].set_title("Original %d" % (yi + 1)) 
    
    plt.tight_layout()  
    plt.savefig('clustered_cpu_metrics.png')  
    # plt.show()  

def cluster_metrics(metrics_list, metrics_data, metric_name = 'cpu'):
    # Get data for all cpu metrics  
    metrics_data = {}  
    
    for metric, metric_info in metrics_list.items():  
        if metric_name in metric.lower():  
            metrics_data[metric] = metrics_data[metric]  
    
    # Prepare data for KShape clustering  
    timeseries_data = []  
    original_timeseries_data = []  # to store original data
    for metric, data in metrics_data.items():  
        if data['data']['result']:  
            values = [float(x[1]) for x in data['data']['result'][0]['values']]  
            original_timeseries_data.append(values)  # store original data 
            timeseries_data.append(values)  
    
    # Rescale the time series data to have zero mean and unit variance  
    timeseries_data = TimeSeriesScalerMeanVariance().fit_transform(timeseries_data)  
    
    # Apply KShape clustering  
    n_clusters = 3  # number of clusters  
    ks = KShape(n_clusters=n_clusters, n_init=50, verbose=True)  
    y_pred = ks.fit_predict(timeseries_data)  
    
    # Plot the clustered time series data  
    fig, axs = plt.subplots(n_clusters, 2, figsize=(10, n_clusters * 5))  
    # If there's only one row of subplots, convert axs to a 2D array  
    if n_clusters == 1:  
        axs = np.array([axs]).reshape(1, -1)
    for yi in range(n_clusters):  
        for xx in timeseries_data[y_pred == yi]:  
            axs[yi].plot(xx.ravel(), "k-", alpha=.2)  

        for xx in original_timeseries_data:  # plot original data in second column  
            axs[yi][1].plot(xx, "k-", alpha=.2)  # plot original data  

        axs[yi][0].plot(ks.cluster_centers_[yi].ravel(), "r-")  
        axs[yi][0].set_title("Cluster %d" % (yi + 1))  
        axs[yi][1].set_title("Original %d" % (yi + 1)) 
    
    plt.tight_layout()  
    plt.savefig(f"clustered_{metric_name}_metrics.png")  
    # plt.show()  