import torch  
import torch  
import pandas as pd  
import numpy as np  
from sklearn.preprocessing import MinMaxScaler  
from sklearn.metrics import r2_score
import requests  
import time
import datetime
import pytz
from sklearn.metrics import mean_absolute_error 
import matplotlib.pyplot as plt

class PredictModule:  
    def __init__(self, ModelClass, config):    
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')    
        self.csv_file = config['csv_file']  
        self.machines_num = config['machines_num']  
        self.lookback_period = config['lookback_period']  
        self.predict_horizontal = config['predict_horizontal']  
        self.train_set_percentage = config['train_set_percentage']  
        self.batch_size = config['batch_size']  
        self.num_epochs = config['num_epochs']  
        self.learning_rate = config['learning_rate']  
        self.input_size = config['input_size']
        self.output_size = config['predict_horizontal']  
        self.data = self.load_data_from_csv()
        if ModelClass.__name__.startswith('mwd'):  
            self.model = ModelClass(self.lookback_period, self.output_size).to(self.device)
        else:  
            self.model = ModelClass(self.input_size, self.output_size).to(self.device)
        self.criterion = torch.nn.MSELoss()    
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate) 
  
    def train(self):
        self.train_inout_seq, self.test_inout_seq = self.create_test_train_data_seq()  

        self.train_model()
        now = datetime.datetime.now()  
        date_str = now.strftime("%Y%m%d%H%M")
        model_name = type(self.model).__name__
        modelname = f"{model_name}_{date_str}.pth"  
        modelpath = f"./pth/{modelname}"
        torch.save(self.model.state_dict(), modelpath)
        print(f"Model saved to {modelpath}")

        self.test_model()  

        return modelpath
  
    
    # Sample Data: 
    # start_time,machine_id,metric_value
    # 2011-05-01 00:10:00,381129,0.9091315
    # 2011-05-01 00:10:00,765912,0.5394293
    def load_data_from_csv(self):
        # Load and preprocess data    
        df = pd.read_csv(self.csv_file)    
        df['start_time'] = pd.to_datetime(df['start_time'])    
        df.set_index('start_time', inplace=True)

        # Select first 10 machines    
        machines = df['machine_id'].unique()[:self.machines_num]  
        df = df[df['machine_id'].isin(machines)]  
        df = df[['machine_id', 'metric_value']]    

        # Scale data to (0, 1) for LSTM    
        self.scaler = MinMaxScaler(feature_range=(0, 1))  
        self.scaler.fit(df['metric_value'].values.reshape(-1,1))  
        df['metric_value'] = self.scaler.transform(df['metric_value'].values.reshape(-1,1))    

        # Convert DataFrame to numpy array    
        data = {machine: df[df['machine_id'] == machine]['metric_value'].values for machine in machines}

        return data
    
    def load_data_from_prometheus(self, start = time.time() - 60 * 3, end = time.time(), metric = 'container_cpu_usage_seconds_total'):
        params = {  
            'query': f'''sum(rate({metric}{{container_label_io_kubernetes_pod_namespace="demo"}}[30s]))''',  
            'start': start,
            'end': end,
            'step': 15,  # define the interval of time (in seconds) between each data point
        }  
    
        response = requests.get('http://localhost:9090/api/v1/query_range', params=params)  
        data = response.json()  
        values = data['data']['result'][0]['values']
        df = pd.DataFrame(values, columns=['timestamp', metric])
        local_tz = datetime.datetime.now(pytz.timezone('UTC')).astimezone().tzinfo 
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert(local_tz)
        df = df.iloc[-self.lookback_period:]  
        print("Load from Prometheus:------------------------------")
        print(df)
        # Drop the timestamp column  
        metric_values = torch.FloatTensor(df[metric].values.astype(float))
        return metric_values  
    
    # Create sequences    
    def create_sequences(self, input_data):    
        inout_seq = []    
        L = len(input_data)    
        for i in range(L-self.lookback_period-self.predict_horizontal):    
            train_seq = torch.FloatTensor(input_data[i:i+self.lookback_period])  
            train_label = torch.FloatTensor(input_data[i+self.lookback_period:i+self.lookback_period+self.predict_horizontal])   
            inout_seq.append((train_seq ,train_label))    
        return inout_seq

    def create_test_train_data_seq(self):
        # Split data into train and test sets    
        train_data = {}  
        test_data = {}  
        for machine in list(self.data.keys()):  
            machine_data = self.data[machine]  
            train_size = int(len(machine_data) * self.train_set_percentage)    
            train_data[machine], test_data[machine] = machine_data[:train_size], machine_data[train_size:]

        train_inout_seq = {machine: self.create_sequences(machine_data) for machine, machine_data in train_data.items()}
        test_inout_seq = {machine: self.create_sequences(machine_data) for machine, machine_data in test_data.items()}  

        return train_inout_seq, test_inout_seq

    def train_model(self):
        self.model.train()
        train_data_loader = {machine: torch.utils.data.DataLoader(machine_inout_seq, batch_size=self.batch_size, shuffle=True) for machine, machine_inout_seq in self.train_inout_seq.items()}    

        for epoch in range(self.num_epochs):   
            sample_num = 0
            squared_error_sum = 0
            absolute_error_sum = 0
            
            for machine_id, data_loader in train_data_loader.items():  
                for i, (seq, labels) in enumerate(data_loader):  
                    # extract one batch of data, here batch is 512
                    # seq sample: 
                    # torch.Size([512, 144])
                    # 144 is the number of seq length, which is the same as look back
                    # 512 is batch size. If we only have 144 data points and set batch size as 512 and set look back 10 and predict 10, then real batch number would be 13.
                    # tensor([[1.1625e-01, 0.0000e+00, 1.3409e-02,  ..., 1.1812e-01, 1.1328e-01,
                    #         1.3212e-01],
                    #         [7.8305e-02, 6.1620e-03, 8.3026e-02,  ..., 8.1897e-02, 8.7666e-02,
                    #         8.1270e-02],
                    #         [0.0000e+00, 7.2096e-03, 1.1042e-01,  ..., 2.8846e-02, 1.0243e-01,
                    #         1.3242e-02],
                    #         ...,
                    #         [0.0000e+00, 1.8987e-03, 0.0000e+00,  ..., 7.1344e-02, 7.5219e-03,
                    #         8.5884e-02],
                    #         [1.1898e-01, 4.4600e-04, 0.0000e+00,  ..., 7.5017e-06, 1.0585e-03,
                    #         2.5554e-04],
                    #         [9.8598e-02, 1.1002e-01, 1.2096e-01,  ..., 7.4919e-02, 8.7025e-02,
                    #         4.7612e-02]]) 
                    seq = torch.FloatTensor(seq).view(-1, self.lookback_period, self.input_size).to(self.device)  
                    # Now the seq shape is (batch_size, lookback_period, input_size) (5, 10, 1)
                    labels = torch.FloatTensor(labels).view(-1, self.predict_horizontal).to(self.device)  
        
                    self.optimizer.zero_grad()    
                    y_pred = self.model(seq)    
        
                    single_loss = self.criterion(y_pred, labels)    
                    squared_error_sum += single_loss.item() * seq.size(0)  # Multiply by batch size  
                    absolute_error = torch.abs(y_pred - labels)
                    absolute_error_sum += absolute_error.sum().item()
                    sample_num += seq.size(0)  
                    single_loss.backward()    
                    self.optimizer.step()    
        
            if (epoch+1)%100 == 0:  
                train_mse = squared_error_sum / sample_num  
                train_rmse = np.sqrt(train_mse)
                train_mae = absolute_error_sum / sample_num
                print('epoch: ', epoch+1, 
                  'train RMSE: ', train_rmse, 
                  'train MSE: ', train_mse, 
                  'train MAE: ', train_mae,  # Print MAE
                  'loss: ', single_loss.item())



    def plot_predictions_vs_actuals(self, predictions, actuals, num_points=200):
        # Ensure predictions and actuals are 1D arrays for plotting
        if predictions.ndim > 1:
            predictions = predictions.ravel()
        if actuals.ndim > 1:
            actuals = actuals.ravel()

        if len(predictions) > num_points:
            predictions = predictions[-num_points:]
            actuals = actuals[-num_points:]

        # Create a new figure
        plt.figure(figsize=(12, 6))

        # Plot actuals and predictions
        plt.plot(actuals, label='Actuals', color='blue', alpha=0.7)
        plt.plot(predictions, label='Predictions', color='red', alpha=0.7)

        # Add titles and labels
        plt.title('Actual vs Predicted Values (Last {} Points)'.format(num_points))
        plt.xlabel('Sample Index')
        plt.ylabel('Value')
        plt.legend()

        # Show the plot
        plt.show()

    def test_model(self):
        self.model.eval()
        test_rmse = 0  
        test_mse = 0  
        ttl = 0  
        predictions = []    
        actuals = []   
        with torch.no_grad():  
            for machine_id, seqs in self.test_inout_seq.items():  
                for seq, labels in seqs:    
                    seq = torch.FloatTensor(seq).view(-1, self.lookback_period, self.input_size).to(self.device)    
                    labels = torch.FloatTensor(labels).view(-1, self.predict_horizontal).to(self.device)    
                    y_test_pred = self.model(seq)    
        
                    # Ensure labels and y_test_pred have the same size    
                    if y_test_pred.shape != labels.shape:    
                        print("Shape mismatch: y_test_pred has shape {} but labels have shape {}".format(y_test_pred.shape, labels.shape))    
                        continue    
        
                    predictions.append(y_test_pred.cpu().detach().numpy())    
                    actuals.append(labels.cpu().detach().numpy())    
        
                    test_loss = self.criterion(y_test_pred, labels)   
                    test_rmse += np.sqrt(test_loss.item())  
                    test_mse += np.mean(test_loss.item())  
                    ttl += 1  
        
        # Flatten the lists of predictions and actuals into 1D arrays    
        predictions = np.concatenate(predictions).ravel()    
        actuals = np.concatenate(actuals).ravel() 

        self.plot_predictions_vs_actuals(predictions, actuals)

        test_mae = mean_absolute_error(actuals, predictions)   
        
        r2 = r2_score(actuals, predictions)    
        
        print('test RMSE: ', test_rmse/ttl, 'test MSE: ', test_mse/ttl, 'test MAE: ', test_mae, 'r2-score: ', r2)

    def generate_test_data(self):  
        # Generate a tensor  
        random_data_to_predict = torch.rand((1, self.lookback_period))  
        print("generate sample data: ", random_data_to_predict)
        return random_data_to_predict

    def predict(self, model_path, input_data):  
        input_data = self.scaler.transform(input_data.reshape(-1,1))    
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))  
        self.model.eval()  
    
        with torch.no_grad():   
            input_data = torch.FloatTensor(input_data).view(-1, self.lookback_period, self.input_size).to(self.device)  
            predictions = self.model(input_data)  
            predictions = self.scaler.inverse_transform(predictions)  
        
        # print("prediction: ", predictions)
        return predictions