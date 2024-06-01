from metrics import load_metrics, save_merics_chart

# 1. DBSCAN (Density-Based Spatial Clustering of Applications with Noise): This algorithm views clusters as areas of high density separated by areas of low density. Due to this rather generic view, clusters found by DBSCAN can be any shape, as opposed to k-means which assumes that clusters are convex shaped. The central component to the DBSCAN is the concept of core samples, which are samples that are in areas of high density.
# 2. HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise): HDBSCAN is an extension of DBSCAN algorithm. Unlike DBSCAN, HDBSCAN does not require you to choose an appropriate value for epsilon, which makes it quite useful in practice.
# 3. Mean Shift Clustering: The Mean Shift Clustering algorithm is a hill-climbing algorithm that involves shifting points towards the mode (highest density of data points). The algorithm automatically sets the number of clusters, instead of requiring the user to specify the number of clusters to be generated.
# 4. Optics Clustering: OPTICS clustering (Ordering Points To Identify the Clustering Structure) is a modified version of DBSCAN described above. It adds two more terms to the concepts of DBSCAN clustering. The two terms are: The Core Distance of a point and the Reachability Distance of a point.
# 5. Affinity Propagation: Affinity Propagation involves finding a set of exemplars that best summarize the data. It operates by sending messages between pairs of samples until convergence. A dataset is then described using a small number of exemplars, which are identified as those most representative of other samples.
# from kshape import cluster_metrics
# from dbscan import cluster_metrics # good
# from hdbscan_m import cluster_metrics # good
# from meanshift import cluster_metrics
# from optics import cluster_metrics 
from affinitypropagation import cluster_metrics # best

metrics_list, metrics_data = load_metrics()

save_merics_chart(metrics_data)

cluster_metrics(metrics_list, metrics_data, 'memory')

# cluster_cpu_metrics(metrics_list, metrics_data)