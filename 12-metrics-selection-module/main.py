from metrics import load_metrics, save_merics_chart
from datetime import datetime  
import argparse  

# 1. DBSCAN (Density-Based Spatial Clustering of Applications with Noise): This algorithm views clusters as areas of high density separated by areas of low density. Due to this rather generic view, clusters found by DBSCAN can be any shape, as opposed to k-means which assumes that clusters are convex shaped. The central component to the DBSCAN is the concept of core samples, which are samples that are in areas of high density.
# 2. HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise): HDBSCAN is an extension of DBSCAN algorithm. Unlike DBSCAN, HDBSCAN does not require you to choose an appropriate value for epsilon, which makes it quite useful in practice.
# 3. Mean Shift Clustering: The Mean Shift Clustering algorithm is a hill-climbing algorithm that involves shifting points towards the mode (highest density of data points). The algorithm automatically sets the number of clusters, instead of requiring the user to specify the number of clusters to be generated.
# 4. Optics Clustering: OPTICS clustering (Ordering Points To Identify the Clustering Structure) is a modified version of DBSCAN described above. It adds two more terms to the concepts of DBSCAN clustering. The two terms are: The Core Distance of a point and the Reachability Distance of a point.
# 5. Affinity Propagation: Affinity Propagation involves finding a set of exemplars that best summarize the data. It operates by sending messages between pairs of samples until convergence. A dataset is then described using a small number of exemplars, which are identified as those most representative of other samples.
# from kshape import cluster_metrics # available, need to manually specify the number of clusters
# from dbscan import cluster_metrics # good
# from hdbscan_m import cluster_metrics # good
# from meanshift import cluster_metrics
# from optics import cluster_metrics 
from affinitypropagation import cluster_metrics # available

# cluster_cpu_metrics(metrics_list, metrics_data)

  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser()  
    parser.add_argument("--start_time", type=str, help="Start time in the format YYYYMMDDHHMMSS")  
    parser.add_argument("--end_time", type=str, help="End time in the format YYYYMMDDHHMMSS")  
    args = parser.parse_args()  

    start_time = datetime.strptime(args.start_time, "%Y%m%d%H%M%S").timestamp()  
    end_time = datetime.strptime(args.end_time, "%Y%m%d%H%M%S").timestamp()  
    now = datetime.now()  
    # Format as %Y%m%d%H%M%S  
    time_string = now.strftime("%Y%m%d%H%M%S") 

    metrics_list, metrics_data = load_metrics(start_time, end_time)

    save_merics_chart(metrics_data, time_string)

    # cluster_metrics(metrics_list, metrics_data, time_string, 'all')

    cluster_metrics(metrics_list, metrics_data, time_string, '_cpu_')
    cluster_metrics(metrics_list, metrics_data, time_string, '_memory_')
    cluster_metrics(metrics_list, metrics_data, time_string, '_network_')
    # cluster_metrics(metrics_list, metrics_data, time_string, '_fs_')
