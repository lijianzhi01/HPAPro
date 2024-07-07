import time
from loader import Loader

loader = Loader()
model = loader.pick("LSTM002CPU")
# 2024-06-27 10:31:00 to 2024-06-27 10:34:00, it must be :00!!!!!
# container_cpu_usage_seconds_total
# container_memory_failures_total
# container_network_transmit_packets_total
metrics_data = model.pm.load_data_from_prometheus(1720353630 - 180, 1720353630, 'container_cpu_usage_seconds_total') 
prediction = model.pm.predict(model.pth, metrics_data)
print(prediction)

model = loader.pick("LSTM002Mem")
metrics_data = model.pm.load_data_from_prometheus(1720353630 - 180, 1720353630, 'container_memory_failures_total') 
prediction = model.pm.predict(model.pth, metrics_data)
print(prediction)


model = loader.pick("LSTM002Metwork")
metrics_data = model.pm.load_data_from_prometheus(1720353630 - 180, 1720353630, 'container_network_transmit_packets_total') 
prediction = model.pm.predict(model.pth, metrics_data)
print(prediction)