import sys  
import math  
from kubernetes import client, config  
from kubernetes.client.rest import ApiException  
  
def scale_deployment(namespace, deployment, predicted_cpu):  
    config.load_kube_config('C:\\Users\\jianzhili\\.kube\\config')
    predicted_cpu = int(1000 * predicted_cpu) # convert to milliCPU
    api_instance = client.AppsV1Api()  
  
    try:  
        api_response = api_instance.read_namespaced_deployment(name=deployment, namespace=namespace)  
        cpu_request_per_pod = api_response.spec.template.spec.containers[0].resources.requests['cpu']  
          
        # Convert the cpu_request_per_pod to milliCPU  
        cpu_request_per_pod_milli = int(cpu_request_per_pod.replace('m', '')) if 'm' in cpu_request_per_pod else int(cpu_request_per_pod) * 1000  
        current_replicas = int(api_response.spec.replicas)
        sum_up_requests = current_replicas * cpu_request_per_pod_milli
  
        if predicted_cpu > sum_up_requests:
            # Calculate the new replica size  
            new_replica_size = math.ceil(predicted_cpu / cpu_request_per_pod_milli)  
            api_response.spec.replicas = new_replica_size  
            # api_instance.patch_namespaced_deployment_scale(name=deployment, namespace=namespace, body=api_response)  
    
            print(f"Scaled deployment {deployment} to {api_response.spec.replicas} replicas. [Predicted CPU: {predicted_cpu}m, Current Requested CPU: {sum_up_requests}m={cpu_request_per_pod_milli}m*{current_replicas}]") 
        else:  
            print("No need to scale the deployment")
  
    except ApiException as e:  
        print(f"Exception when calling AppsV1Api->read_namespaced_deployment: {e}")  
  
if __name__ == "__main__":  
    if len(sys.argv) != 4:  
        print(f"Usage: {sys.argv[0]} <namespace> <deployment> <predicted_cpu>")  
        sys.exit(1)  
  
    scale_deployment(sys.argv[1], sys.argv[2], float(sys.argv[3]))
