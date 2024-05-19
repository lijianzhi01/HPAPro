import requests    
import time    
import json    
import matplotlib.pyplot as plt    
from metrics import load_metrics, save_merics_chart
from kshape import cluster_cpu_metrics

metrics_list, metrics_data = load_metrics()

save_merics_chart(metrics_data)

cluster_cpu_metrics(metrics_list, metrics_data)