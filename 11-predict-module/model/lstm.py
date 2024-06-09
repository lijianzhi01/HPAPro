import torch  
import torch.nn as nn 

# Define LSTM model  
class LSTM(nn.Module):  
    def __init__(self, input_size, output_size):  
        super(LSTM, self).__init__()  
        self.hidden_size = 10  
        self.num_layers = 1  
  
        self.lstm = nn.LSTM(input_size, self.hidden_size, self.num_layers, batch_first=True)  
        self.fc = nn.Linear(self.hidden_size, output_size)  
  
    def forward(self, x):  
        h_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)  
        c_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)  
  
        out, _ = self.lstm(x, (h_0, c_0))  
        out = self.fc(out[:, -1, :])  
  
        return out 