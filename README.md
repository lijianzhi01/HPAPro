# HPAPro
For Graduate Paper


## 
```bash
minikube dashboard 

kubectl -n grafana port-forward svc/grafana 3000

kubectl port-forward svc/prometheus-operated 9090 -n monitoring

minikube service express -n demo
```


## Build App
```bash
cd 0-express
docker build . -t lijianzhi01/app:0.0.1
docker push lijianzhi01/app:0.0.1

# deprecated
cd 10-simulation/app
docker build . -t lijianzhi01/simulation:0.0.3
```

## Deploy Mongodb (deprecated)
### Set up secret
```bash
# Git Bash
kubectl create secret generic mongodb-secret --from-literal=mongo-root-username='jianzhili' -n demo
kubectl patch secret mongodb-secret --type=merge --patch='{"stringData":{"mongo-root-password":"123456"}}' -n demo
```

## Metrics Selection Module
```bash
cd 12-metrics-selection-module
py main.py
```

## Run Simulation
```bash
cd 10-simulation
py .\load_simulation_with_pattern.py onoff  54155
```

# Experiement for Predictable HPA
### Step One: Generate Simulation

Use [generator](./10-simulation/static_sim/rps_generator.py) to create sample data for either bursting or variations pattern. 
```pwsh
py .\rps_generator.py bursting 3600
py .\rps_generator.py variations 3600
```

Use [play](./10-simulation/static_sim/play_requests.py) to simulate.
```pwsh
py .\play_requests.py bursting-240616-154338.txt 62795
```

Use to generate CPU and Memory metrics data. 
```pwsh
cd 11-predict-module
py .\export_metrics.py --start_time 20240616001300 --end_time 20240616002515 --pattern bursting
```

### Step Two: Train module

### Step Three: Play and Predict
Use [play](./10-simulation/static_sim/play_requests.py) to simulate.

Use module to predict and scale application. 

Check SLA.