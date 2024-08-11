import time
from loader import Loader

loader = Loader()
model = loader.pick("MF-LSTM-Attention001")
pth = model.train()

# loader = Loader()
# model = loader.pick("BILSTMGCT")
# pth = model.train()

# loader = Loader()
# model = loader.pick("MWDLSTMGCT")
# pth = model.train()