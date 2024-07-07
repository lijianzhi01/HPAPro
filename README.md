# HPAPro
For Graduate Paper

# 1 Set up Env

## 1.1 Initialize minikube
```bash
minikube start

minikube dashboard

kubectl -n grafana port-forward svc/grafana 3000

kubectl port-forward svc/prometheus-operated 9090 -n monitoring

minikube service express -n demo
```


## 1.2 Build and Release App
```bash
cd 0-express
docker build . -t lijianzhi01/app:0.0.14
docker push lijianzhi01/app:0.0.14

kubectl apply -f ./5-demo/0-deployment.yaml
```


## 1.3 Metrics Selection Module
```bash
cd 12-metrics-selection-module
py ./main.py --start_time 20240707234000 --end_time 20240707235845
```

## 1.4 Open Simulation
```bash
~/repo/apache-jmeter-5.6.3/bin/jmeter.bat
```

# 2 Train Predictive HPA
## 2.1 Start Simulation in JMeter
```bash
cd ./10-simulation/jmeter
# load BurstingPattern.jmx
```

## 2.2 Export Metrics from Prometheus
```bash
cd 11-predict-module
py ./export_metrics.py --start_time 20240707195645 --end_time 20240707201445 --pattern bursting --metric container_cpu_usage_seconds_total
py ./export_metrics.py --start_time 20240707195645 --end_time 20240707201445 --pattern bursting --metric container_memory_failures_total
py ./export_metrics.py --start_time 20240707195645 --end_time 20240707201445 --pattern bursting --metric container_network_transmit_packets_total
```

## 2.3 Train Model
Add Model Config in 11-predict-module/loader
```bash
# train model
py ./train_model.py
# get model path and fill in back to loader, then make prediction
py ./validate_model.py
```


# 3 Start Experiment

## 3.1 Initialize Test Case

### 3.1.1 K8s Native HPA
```bash
kubectl apply -f 5-demo/hpa-http-requests.yaml
```

### 3.1.2 Prediction with LSTM
```bash
kubectl delete hpa http -n demo
py ./lstm_scaler.py
```

### 3.1.3 Prediction with LSTM+Attention
```bash
kubectl delete hpa http -n demo
py ./predict_and_evaluate.py
```

### 3.1.4 Prediction with LSTM+Attention+MSM (TBD)
```bash
kubectl delete hpa http -n demo
py ./msm_lstm_scaler.py
```


## 3.2 Start Simulation in JMeter
```bash
cd ./10-simulation/jmeter
# load BurstingPattern.jmx
~/repo/apache-jmeter-5.6.3/bin/jmeter.bat
```

## 3.3 Check Metrics
* P95 in `10-simulation/jmeter/JUnitReport`
* Calc Violations
* CPU usage in grafana
    ```bash
    cd 10-simulation
    py ./ave_pod_cpu_usage.py --start_time 20240707202900 --end_time 20240707204700
    ```