import math
import torch
import torch.nn as nn
import torch.nn.functional as F 
from torch.autograd import Variable
import numpy as np 
from model.utils import ToVariable

class SelfAttention(nn.Module):  
    def __init__(self, hidden_size):  
        super(SelfAttention, self).__init__()  
        self.hidden_size = hidden_size  
        self.attn_weights = nn.Parameter(torch.Tensor(1, hidden_size))  
        stdv = 1. / math.sqrt(self.attn_weights.size(0))  
        self.attn_weights.data.uniform_(-stdv, stdv)  
        self.softmax = nn.Softmax(dim=-1)  
  
    def forward(self, inputs):  
        attn_scores = torch.matmul(inputs, self.attn_weights.permute(1,0))  
        attn_scores = self.softmax(attn_scores)  
        outputs = torch.bmm(attn_scores.transpose(1,2), inputs).squeeze(1)  
        return outputs  


# This model only implements two levels of decomposition
class MWDLSTMGCT(nn.Module):
    def __init__(self,seq_len,output_size):
        super(MWDLSTMGCT,self).__init__()
        self.seq_len = seq_len
        self.hidden_size = 100
        self.output_size = output_size

        self.attn = SelfAttention(self.hidden_size)
        self.mWDN1_H = nn.Linear(seq_len,seq_len)
        self.mWDN1_L = nn.Linear(seq_len,seq_len)
        self.mWDN2_H = nn.Linear(int(seq_len/2),int(seq_len/2))
        self.mWDN2_L = nn.Linear(int(seq_len/2),int(seq_len/2))
        self.a_to_x = nn.AvgPool1d(2)
        self.sigmoid = nn.Sigmoid()
        self.lstm_xh1 = nn.LSTM(1,self.hidden_size,batch_first=True)
        self.lstm_xh2 = nn.LSTM(1,self.hidden_size,batch_first=True)
        self.lstm_xl2 = nn.LSTM(1,self.hidden_size,batch_first=True)
        self.output = nn.Linear(self.hidden_size,output_size)

        self.l_filter = [-0.0106,0.0329,0.0308,-0.187,-0.028,0.6309,0.7148,0.2304]
        self.h_filter = [-0.2304,0.7148,-0.6309,-0.028,0.187,0.0308,-0.0329,-0.0106]

        self.cmp_mWDN1_H = ToVariable(self.create_W(seq_len,False,is_comp=True))
        self.cmp_mWDN1_L = ToVariable(self.create_W(seq_len,True,is_comp=True))
        self.cmp_mWDN2_H = ToVariable(self.create_W(int(seq_len/2),False,is_comp=True))
        self.cmp_mWDN2_L = ToVariable(self.create_W(int(seq_len/2),True,is_comp=True))

        self.mWDN1_H.weight = torch.nn.Parameter(ToVariable(self.create_W(seq_len,False)))
        self.mWDN1_L.weight = torch.nn.Parameter(ToVariable(self.create_W(seq_len,True)))
        self.mWDN2_H.weight = torch.nn.Parameter(ToVariable(self.create_W(int(seq_len/2),False)))
        self.mWDN2_L.weight = torch.nn.Parameter(ToVariable(self.create_W(int(seq_len/2),True)))

    def forward(self,input):
        # init_state parameter is batch_size
        h1,c1,h2,c2,h3,c3 = self.init_state(input.shape[0])
        # input shape is [batch_size,seq_len], we need to remove third dimension: seq_len
        input = input[:,:,-1]
        ah_1 = self.sigmoid(self.mWDN1_H(input))
        al_1 = self.sigmoid(self.mWDN1_L(input))
        xh_1 = self.a_to_x(ah_1.view(ah_1.shape[0],1,-1))
        xl_1 = self.a_to_x(al_1.view(al_1.shape[0],1,-1))
        
        ah_2 = self.sigmoid(self.mWDN2_H(xl_1))
        al_2 = self.sigmoid(self.mWDN2_L(xl_1))
        
        xh_2 = self.a_to_x(ah_2)
        xl_2 = self.a_to_x(al_2)

        xh_1 = xh_1.transpose(1,2)
        xh_2 = xh_2.transpose(1,2)
        xl_2 = xl_2.transpose(1,2)

        level1_lstm,(h1,c1) = self.lstm_xh1(xh_1,(h1,c1))
        level2_lstm_h,(h2,c2) = self.lstm_xh2(xh_2,(h2,c2))
        level2_lstm_l,(h3,c3) = self.lstm_xl2(xl_2,(h3,c3))

        # output = self.output(torch.cat((level1_lstm,level2_lstm_h,level2_lstm_l), 1))
        concat_output = torch.cat((level1_lstm,level2_lstm_h,level2_lstm_l), 1)
        output = self.output(concat_output)
        return output[:,-1,:]

    def init_state(self,batch_size):
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')  
  
        h1 = Variable(torch.zeros(1, batch_size, self.hidden_size)).float().to(device)  
        c1 = Variable(torch.zeros(1, batch_size, self.hidden_size)).float().to(device)  
    
        h2 = Variable(torch.zeros(1, batch_size, self.hidden_size)).float().to(device)  
        c2 = Variable(torch.zeros(1, batch_size, self.hidden_size)).float().to(device)  
    
        h3 = Variable(torch.zeros(1, batch_size, self.hidden_size)).float().to(device)  
        c3 = Variable(torch.zeros(1, batch_size, self.hidden_size)).float().to(device)  
        
        return h1, c1, h2, c2, h3, c3 

    def create_W(self,P,is_l,is_comp=False):
        if is_l : 
            filter_list = self.l_filter
        else:
            filter_list = self.h_filter

        list_len = len(filter_list)

        max_epsilon = np.min(np.abs(filter_list))
        if is_comp:
            weight_np = np.zeros((P,P))
        else:
            weight_np = np.random.randn(P,P)*0.1*max_epsilon

        for i in range(0,P):
            filter_index = 0
            for j in range(i,P):
                if filter_index < len(filter_list):
                    weight_np[i][j] = filter_list[filter_index]
                    filter_index += 1
        return weight_np