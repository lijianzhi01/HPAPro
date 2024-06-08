import pandas as pd  
import numpy as np  
from sklearn.preprocessing import MinMaxScaler  
from keras.models import Sequential  
from keras.layers import LSTM, Dense  
  
# Load your data  
df = pd.read_csv('cpu_usage_per_machine.csv')  
  
# For the purpose of the example, I'm assuming the data is already loaded into 'df'  
# original data looks like this:
#             start_time  machine_id  maximum_cpu_usage
# 0  2011-05-01 00:10:00      381129           0.909131
# 1  2011-05-01 00:10:00      765912           0.539429
df['start_time'] = pd.to_datetime(df['start_time'])  
# set the index to be the date
#                      machine_id  maximum_cpu_usage
# start_time
# 2011-05-01 00:10:00      381129           0.909131
# 2011-05-01 00:10:00      765912           0.539429
df.set_index('start_time', inplace=True)  
  
# Scale your data  
scaler = MinMaxScaler(feature_range=(0,1))
# scaled_data looks like this:  
# [[0.01665592]
#  [0.00988272]
#  [0.01105831]
#  [0.00041936]
#  [0.01263697]]
scaled_data = scaler.fit_transform(df['maximum_cpu_usage'].values.reshape(-1,1))  
print(scaled_data[:5])
  
# Create your LSTM model  
# The Sequential model is a type of model provided by Keras, which is appropriate for a plain stack of layers where each layer has exactly one input tensor and one output tensor.

# When you're building a neural network, you're essentially stacking layers of neurons on top of each other. The Sequential model is a way to set up your network as a linear stack of layers, 
# meaning that you can create your network layer by layer in a sequential manner.
model = Sequential()  
model.add(LSTM(units=50, input_shape=(None, 1)))
model.add(Dense(1))  
  
model.compile(loss='mean_squared_error', optimizer='adam')  
  
# Prepare your dataset for LSTM  
def create_dataset(X, time_steps_in=1, time_steps_out=1):  
    Xs, ys = [], []  
    for i in range(len(X) - time_steps_in - time_steps_out + 1):  
        Xs.append(X[i:(i + time_steps_in)])  
        ys.append(X[(i + time_steps_in):(i + time_steps_in + time_steps_out)])  
    return np.array(Xs), np.array(ys)  
  
time_steps_in = 30  
time_steps_out = 10  
  
# Split the data into train and test sets  
train_size = int(len(scaled_data) * 0.7)  
test_size = len(scaled_data) - train_size  
train, test = scaled_data[0:train_size,:], scaled_data[train_size:len(scaled_data),:]  
  
trainX, trainY = create_dataset(train, time_steps_in, time_steps_out)  
testX, testY = create_dataset(test, time_steps_in, time_steps_out)
  
# Reshape input to be [samples, time steps, features]  
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))  
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))  
  
# Train your model  
model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)  
  
# Make predictions  
trainPredict = model.predict(trainX)  
testPredict = model.predict(testX)  
  
# Invert predictions to original scale  
trainPredict = scaler.inverse_transform(trainPredict)  
trainY = scaler.inverse_transform([trainY])  
testPredict = scaler.inverse_transform(testPredict)  
testY = scaler.inverse_transform([testY])  
