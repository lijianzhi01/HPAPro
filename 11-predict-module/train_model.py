import time
from loader import Loader

loader = Loader()
model = loader.pick("LSTMGCT")
pth = model.train()

# loader = Loader()
# model = loader.pick("BILSTMGCT")
# pth = model.train()

# loader = Loader()
# model = loader.pick("MWDLSTMGCT")
# pth = model.train()