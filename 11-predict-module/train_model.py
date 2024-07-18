import time
from loader import Loader

loader = Loader()
model = loader.pick("LSTM002")
pth = model.train()