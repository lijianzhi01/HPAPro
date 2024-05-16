# HPAPro
For Graduate Paper


## 
```bash
minikube dashboard 

kubectl -n grafana port-forward svc/grafana 3000

kubectl port-forward svc/prometheus-operated 9090 -n monitoring
```

## Build App
```bash
cd 0-express
docker build . -t lijianzhi01/app:0.0.1
docker push lijianzhi01/app:0.0.1

cd 10-simulation
docker build . -t lijianzhi01/simulation:0.0.3
```

