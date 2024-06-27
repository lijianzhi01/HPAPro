# HPAPro
For Graduate Paper


## 1.1 Set up MAPE
```bash
minikube dashboard 

kubectl -n grafana port-forward svc/grafana 3000

kubectl port-forward svc/prometheus-operated 9090 -n monitoring

minikube service express -n demo
```


## 1.2. Build App
```bash
cd 0-express
docker build . -t lijianzhi01/app:0.0.1
docker push lijianzhi01/app:0.0.1
```

## 1.3 Metrics
### 1.3.1 Use Histogram
```js
const responseTimes = new Histogram({  
  name: 'http_response_time_seconds',  
  help: 'Histogram of http response durations',  
  labelNames: ['method', 'status_code'],  
  buckets: [100, 200, 400, 800] // Buckets for response time from 0.1s to 5s  
});

responseTimes.observe({ method: 'POST', status_code: res.statusCode}, responseTime); // Record to histogram, convert ms to seconds  

```
```bash
curl -d '{"number": 36}' -H "Content-Type: application/json" -s "http://127.0.0.1:62795/fibonacci"
```
### 1.3.1.1 _bucket
```bash
http_response_time_seconds_sum{namespace="demo"}[45s]
```
counter of less equal than xx for each bucket
```python
# three points mean metric is collected every 15 seconds
http_response_time_seconds_bucket{le="100",namespace="demo"}
0 @1718634262.3
0 @1718634277.299
0 @1718634292.299
 
http_response_time_seconds_bucket{le="200",namespace="demo"}
0 @1718634262.3
0 @1718634277.299
0 @1718634292.299
 
# this bucket adds 1 because we send one request
http_response_time_seconds_bucket{le="400",namespace="demo"}
1 @1718634262.3
2 @1718634277.299
2 @1718634292.299
 
# this bucket adds 1 because less equal 800 has one more element
http_response_time_seconds_bucket{le="800",namespace="demo"}
1 @1718634262.3
2 @1718634277.299
2 @1718634292.299
 
http_response_time_seconds_bucket{le="+Inf",namespace="demo"}
1 @1718634262.3
2 @1718634277.299
2 @1718634292.299
```

## 1.3.1.2 _count
```bash
http_response_time_seconds_count[1m]
```
all requests
```python
http_response_time_seconds_count{container="express", endpoint="http", instance="10.244.0.255:8081", job="express", method="POST", namespace="demo", pod="express-5d64bd45cc-gj98b", service="express", status_code="200"}
1 @1718634232.298
1 @1718634247.301
1 @1718634262.3
2 @1718634277.299
```

### 1.3.1.3 _sum
```bash
http_response_time_seconds_sum{namespace="demo"}[45s]  
```
increase 10 which is response time for one time
```python
# The second request takes 324 = 615 - 291 seconds
http_response_time_seconds_sum{namespace="demo"}
291 @1718634262.3
615 @1718634277.299
615 @1718634292.299
```

### 1.3.2 Use both Histogram and Summary to get percentile

https://prometheus.io/docs/practices/histograms/

## 1.4 Deploy Mongodb (deprecated)
### Set up secret
```bash
# Git Bash
kubectl create secret generic mongodb-secret --from-literal=mongo-root-username='jianzhili' -n demo
kubectl patch secret mongodb-secret --type=merge --patch='{"stringData":{"mongo-root-password":"123456"}}' -n demo
```

## 1.5 Metrics Selection Module
```bash
cd 12-metrics-selection-module
py main.py
```

## 1.6 Run Simulation
```bash
cd 10-simulation
py .\load_simulation_with_pattern.py onoff  54155
```

# 2. Experiement for Predictable HPA
### Step One: Generate Simulation (deprecated)

Use [generator](./10-simulation/static_sim/rps_generator.py) to create sample data for either bursting or variations pattern. 
```pwsh
cd 10-simulation\static_sim\
py .\rps_generator.py bursting 3600
py .\rps_generator.py variations 3600
```

Use [play](./10-simulation/static_sim/play_requests.py) to simulate.
```pwsh
cd 10-simulation\static_sim\
py .\play_requests.py bursting-240616-154338.txt 62795
```

Use to generate CPU and Memory metrics data. 
```pwsh
cd 11-predict-module
py .\export_metrics.py --start_time 20240616001300 --end_time 20240616002515 --pattern bursting
```

### Step One: Simulation with JMeter
TBD

### Step Two: Train module

### Step Three: Play and Predict
Use [play](./10-simulation/static_sim/play_requests.py) to simulate.

Use module to predict and scale application. 

Check SLA.
```pwsh
cd 7-cadvisor
py .\metrics_loader.py --start_time 1718554172 --threshold 0.1
```

# 3. Run the Simulation
```bash
py ./start_experiment.py # deprecated
py ./predict_and_evaluate.py
```