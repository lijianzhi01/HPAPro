import time
from loader import Loader

loader = Loader()
model = loader.pick("LSTMGCT")
pth = model.train()