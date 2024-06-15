# Run simulation locally instead of k8s deployment
If you are running a Kubernetes service on Minikube, you can access it from your host computer using the `minikube service` command followed by the service name. This command will open up the service in your default browser. Here are the steps:  
   
1. Open a terminal.  
   
2. First, make sure that Minikube is running using the following command:  
   ```  
   minikube status  
   ```  
3. If Minikube is running, you can get a list of your services with the following command:  
   ```  
   kubectl get services -n demo
   ```  
4. Now, use the `minikube service` command followed by your service name to access the service. For example, if your service name is `my-service`, you would use:  
   ```bash
   minikube service express -n demo
   ```
   ```
   W0602 16:14:23.642812    7584 main.go:291] Unable to resolve the current Docker CLI context "default": context "default": context not found: open C:\Users\jianzhili\.docker\contexts\meta\37a8eec1ce19687d132fe29051dca629d164e2c4958ba141d5f4133a33f0688f\meta.json: The system cannot find the path specified.
    |-----------|---------|-------------|---------------------------|
    | NAMESPACE |  NAME   | TARGET PORT |            URL            |
    |-----------|---------|-------------|---------------------------|
    | demo      | express | http/8081   | http://192.168.49.2:32393 |
    |-----------|---------|-------------|---------------------------|
    * 为服务 express 启动隧道。
    |-----------|---------|-------------|------------------------|
    | NAMESPACE |  NAME   | TARGET PORT |          URL           |
    |-----------|---------|-------------|------------------------|
    | demo      | express |             | http://127.0.0.1:54155 |
    |-----------|---------|-------------|------------------------|
   ```
    ```bash
    curl -d '{"number": 30}' -H "Content-Type: application/json" -s "http://127.0.0.1:54155/fibonacci"
    ```


# Static Simulation
1. Generate RPS
   ```pwsh
   py .\rps_generator.py bursting 3600
   py .\rps_generator.py variations 3600
   ```

2. Playback to Generate Simulation Data
   ```pwsh
   py .\play_requests.py bursting-240615-222015.txt 62795
   ```