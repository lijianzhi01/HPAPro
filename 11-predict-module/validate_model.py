import time
from loader import Loader

loader = Loader()
model = loader.pick("Lstm001")
# 2024-06-27 10:31:00 to 2024-06-27 10:34:00, it must be :00!!!!!
cpu_data = model.pm.load_data_from_prometheus(1719455640 - 180, 1719455640) 
prediction = model.pm.predict(model.pth, cpu_data)
print(prediction)