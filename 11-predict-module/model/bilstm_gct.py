import torch  
import torch.nn as nn 

# Define LSTM model  
class BiLSTMGCT(nn.Module):  
    def __init__(self, input_size, output_size):  
        super(BiLSTMGCT, self).__init__()  
        self.hidden_size = 100  
        self.num_layers = 1  
        self.bidirectional = True  # Enable bidirectional mode
  
        # Initialize Bi-LSTM
        self.lstm = nn.LSTM(input_size, self.hidden_size, self.num_layers, 
                            batch_first=True, bidirectional=self.bidirectional)
        
        # Update the hidden size for the fully connected layer
        self.fc = nn.Linear(self.hidden_size * 2, output_size)  # *2 because of bidirectionality
        
        self.softplus = nn.Softplus()
  
    def forward(self, x):  
        h_0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(x.device)  # *2 for bidirectional
        c_0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(x.device)  # *2 for bidirectional
  
        out, _ = self.lstm(x, (h_0, c_0))  
        out = self.fc(out[:, -1, :])  # Use the last time step
        out = self.softplus(out)  # Apply Softplus activation function
  
        return out