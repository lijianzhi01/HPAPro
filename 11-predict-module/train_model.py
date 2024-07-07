import time
from loader import Loader

loader = Loader()
model = loader.pick("LSTM002CPU")
pth = model.train()

model = loader.pick("LSTM002Mem")
pth = model.train()

model = loader.pick("LSTM002Metwork")
pth = model.train()
