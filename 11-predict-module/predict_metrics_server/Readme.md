# 1 Set up App
## 1.1 Build App
```bash
cd 0-express
docker build . -t lijianzhi01/predictapp:0.0.1
docker push lijianzhi01/predictapp:0.0.1
```

## 1.2 Deploy App
```bash
cd 5-demo
kubectl apply -f .
```

# 2 Upload Metrics
## 2.1 Initiating service
```bash
minikube service predictapp -n demo

```

## 2.1 Send metrics
```bash
curl -d '{"number": 20}' -H "Content-Type: application/json" -s "http://127.0.0.1:61228/set_future_cpu_usage"
```