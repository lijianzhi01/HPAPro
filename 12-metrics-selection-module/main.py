import requests    
import time    
import json    
import matplotlib.pyplot as plt    
from metrics import load_metrics, save_merics_chart

all_metrics_data = load_metrics()

save_merics_chart(all_metrics_data)
