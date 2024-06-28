import time
from loader import Loader

loader = Loader()
model = loader.pick("LSTM001")
pth = model.train()
