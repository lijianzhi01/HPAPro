import time
from loader import Loader

loader = Loader()
model = loader.pick("Lstm001")
pth = model.train()
