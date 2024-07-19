import time
from loader import Loader

loader = Loader()
model = loader.pick("MWDLSTM001")
pth = model.train()