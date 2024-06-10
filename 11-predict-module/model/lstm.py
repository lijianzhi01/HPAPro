import torch  
import torch.nn as nn 

# Define LSTM model  
class LSTM(nn.Module):  
    def __init__(self, input_size, output_size):  
        super(LSTM, self).__init__()  
        self.hidden_size = 50  
        self.num_layers = 1  
  
        self.lstm = nn.LSTM(input_size, self.hidden_size, self.num_layers, batch_first=True)  
        self.fc = nn.Linear(self.hidden_size, output_size)  
        # a smooth approximation of the ReLU function
        # generate sample data:  tensor([[0.9248, 0.1582, 0.2404, 0.7944, 0.7635, 0.3363, 0.1928, 0.2153, 0.3212,
        #  0.0876, 0.9856, 0.0225, 0.0538, 0.7523, 0.8139, 0.1584, 0.4785, 0.8803,
        #  0.1472, 0.7491, 0.9935, 0.6119, 0.4541, 0.6412, 0.8609, 0.7992, 0.2424,
        #  0.5173, 0.4616, 0.5373, 0.6021, 0.0469, 0.9659, 0.2098, 0.9359, 0.9887,
        #  0.3144, 0.2710, 0.6855, 0.6080, 0.9606, 0.6158, 0.5747, 0.9033, 0.0013,
        #  0.2489, 0.0048, 0.1953, 0.6332, 0.1948, 0.0468, 0.1810, 0.6588, 0.4561,
        #  0.4893, 0.0292, 0.4391, 0.1404, 0.4590, 0.1957, 0.1211, 0.1035, 0.4153,
        #  0.1327, 0.7432, 0.5496, 0.5372, 0.1518, 0.4690, 0.4071, 0.1581, 0.1455,
        #  0.8448, 0.6896, 0.6119, 0.4915, 0.1706, 0.1673, 0.0688, 0.3315, 0.0567,
        #  0.7210, 0.4149, 0.2552, 0.9975, 0.7347, 0.9416, 0.9396, 0.6336, 0.3027,
        #  0.9529, 0.5825, 0.9448, 0.3709, 0.9976, 0.9530, 0.9746, 0.4288, 0.4158,
        #  0.7607, 0.9866, 0.9569, 0.7924, 0.5526, 0.7402, 0.9612, 0.3519, 0.5058,
        #  0.6102, 0.3024, 0.1249, 0.3230, 0.6932, 0.4813, 0.7005, 0.2849, 0.1560,
        #  0.5035, 0.1031, 0.9622, 0.7983, 0.8660, 0.2070, 0.4396, 0.2642, 0.4224,
        #  0.2469, 0.6948, 0.3217, 0.9883, 0.8830, 0.0976, 0.3777, 0.7866, 0.3774,
        #  0.8690, 0.8656, 0.8984, 0.6038, 0.4025, 0.8217, 0.9893, 0.5018, 0.5508]])
        # prediction:  tensor([[0.0110, 0.1220, 0.1340, 0.1506, 0.2182, 0.1266]], device='cuda:0')
        self.softplus = nn.Softplus()
  
    def forward(self, x):  
        h_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)  
        c_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)  
  
        out, _ = self.lstm(x, (h_0, c_0))  
        out = self.fc(out[:, -1, :])  
        out = self.softplus(out)  # Apply Softplus activation function 
  
        return out 