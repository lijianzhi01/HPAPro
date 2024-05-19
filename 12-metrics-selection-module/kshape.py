# pip install tslearn  
import matplotlib.pyplot as plt
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
    for metric, data in cpu_metrics_data.items():  
        if data['data']['result']:  
            values = [float(x[1]) for x in data['data']['result'][0]['values']]  
            timeseries_data.append(values)  
    
    # Rescale the time series data to have zero mean and unit variance  
    timeseries_data = TimeSeriesScalerMeanVariance().fit_transform(timeseries_data)  
    
    # Apply KShape clustering  
    n_clusters = 2  # number of clusters  
    ks = KShape(n_clusters=n_clusters, n_init=10, verbose=True)  
    y_pred = ks.fit_predict(timeseries_data)  
    
    # Plot the clustered time series data  
    fig, axs = plt.subplots(n_clusters, 1, figsize=(10, n_clusters * 5))  
    for yi in range(n_clusters):  
        for xx in timeseries_data[y_pred == yi]:  
            axs[yi].plot(xx.ravel(), "k-", alpha=.2)  
        axs[yi].plot(ks.cluster_centers_[yi].ravel(), "r-")  
        axs[yi].set_title("Cluster %d" % (yi + 1))  
    
    plt.tight_layout()  
    plt.savefig('clustered_cpu_metrics.png')  
    plt.show()  