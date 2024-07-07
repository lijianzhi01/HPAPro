import sys  
import math  
from kubernetes import client, config  
from kubernetes.client.rest import ApiException  

# use requests to scale out
def scale_deployment(namespace, deployment, predicted_cpu, current_cpu):  
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
  
        if predicted_cpu > sum_up_requests * 0.7:
            # Calculate the new replica size  
            new_replica_size = math.ceil(predicted_cpu / cpu_request_per_pod_milli) 
            if (new_replica_size <= current_replicas):
                print("[Warning] No need to scale in the deployment")
            else: 
                api_response.spec.replicas = new_replica_size  
                api_instance.patch_namespaced_deployment_scale(name=deployment, namespace=namespace, body=api_response)  
                print(f"Scale out deployment {deployment} to {api_response.spec.replicas} replicas. [Predicted CPU: {predicted_cpu}m, Current Requested CPU: {sum_up_requests}m={cpu_request_per_pod_milli}m*{current_replicas}]") 
        elif predicted_cpu <= sum_up_requests * 0.7 and current_cpu <= sum_up_requests * 0.7:
            new_replica_size = math.ceil(predicted_cpu / cpu_request_per_pod_milli) 
            if (new_replica_size >= current_replicas):
                print("[Warning] No need to scale out the deployment")
            else: 
                api_response.spec.replicas = new_replica_size  
                api_instance.patch_namespaced_deployment_scale(name=deployment, namespace=namespace, body=api_response)  
                print(f"Scale in deployment {deployment} to {api_response.spec.replicas} replicas. [Predicted CPU: {predicted_cpu}m, Current Requested CPU: {sum_up_requests}m={cpu_request_per_pod_milli}m*{current_replicas}]") 
        else:
            print("No need to scale the deployment")
  
    except ApiException as e:  
        print(f"Exception when calling AppsV1Api->read_namespaced_deployment: {e}")  

# use limits to scale out
def scale_deployment_v2(namespace, deployment, predicted_cpu, current_cpu):  
    config.load_kube_config('C:\\Users\\jianzhili\\.kube\\config')
    predicted_cpu = int(1000 * predicted_cpu) # convert to milliCPU
    api_instance = client.AppsV1Api()  
  
    try:  
        api_response = api_instance.read_namespaced_deployment(name=deployment, namespace=namespace)  
        cpu_limit_per_pod = api_response.spec.template.spec.containers[0].resources.limits['cpu']  
          
        # Convert the cpu_limit_per_pod to milliCPU  
        cpu_limit_per_pod_milli = int(cpu_limit_per_pod.replace('m', '')) if 'm' in cpu_limit_per_pod else int(cpu_limit_per_pod) * 1000  
        current_replicas = int(api_response.spec.replicas)
        sum_up_requests = current_replicas * cpu_limit_per_pod_milli
  
        if predicted_cpu > sum_up_requests * 0.7:
            # Calculate the new replica size  
            new_replica_size = math.ceil(predicted_cpu / cpu_limit_per_pod_milli) 
            if (new_replica_size <= current_replicas):
                print("[Warning] No need to scale in the deployment")
            else: 
                api_response.spec.replicas = new_replica_size  
                api_instance.patch_namespaced_deployment_scale(name=deployment, namespace=namespace, body=api_response)  
                print(f"Scale out deployment {deployment} to {api_response.spec.replicas} replicas. [Predicted CPU: {predicted_cpu}m, Current Limited CPU: {sum_up_requests}m={cpu_limit_per_pod_milli}m*{current_replicas}]") 
        # elif predicted_cpu <= sum_up_requests * 0.7 and current_cpu <= sum_up_requests * 0.7:
        #     new_replica_size = math.ceil(predicted_cpu / cpu_limit_per_pod_milli) 
        #     if (new_replica_size >= current_replicas):
        #         print("[Warning] No need to scale out the deployment")
        #     else: 
        #         api_response.spec.replicas = new_replica_size  
        #         api_instance.patch_namespaced_deployment_scale(name=deployment, namespace=namespace, body=api_response)  
        #         print(f"Scaled in deployment {deployment} to {api_response.spec.replicas} replicas. [Predicted CPU: {predicted_cpu}m, Current Limited CPU: {sum_up_requests}m={cpu_limit_per_pod_milli}m*{current_replicas}]") 
        else:
            print("No need to scale the deployment")
  
    except ApiException as e:  
        print(f"Exception when calling AppsV1Api->read_namespaced_deployment: {e}")  

# use limits to scale out
def scale_deployment_v3(namespace, deployment, predicted_cpu, predicted_memory_failures, predicted_network_transmit_packets):  
    config.load_kube_config('C:\\Users\\jianzhili\\.kube\\config')
    predicted_cpu = int(1000 * predicted_cpu) # convert to milliCPU
    api_instance = client.AppsV1Api()  
  
    try:  
        api_response = api_instance.read_namespaced_deployment(name=deployment, namespace=namespace)  
        cpu_limit_per_pod = api_response.spec.template.spec.containers[0].resources.limits['cpu'] 
        mem_failure_limit_per_pod = 900
        network_transmit_packets_limit_per_pod = 200 
          
        # Convert the cpu_limit_per_pod to milliCPU  
        cpu_limit_per_pod_milli = int(cpu_limit_per_pod.replace('m', '')) if 'm' in cpu_limit_per_pod else int(cpu_limit_per_pod) * 1000  
        current_replicas = int(api_response.spec.replicas)
        sum_up_requests = current_replicas * cpu_limit_per_pod_milli
        sum_up_mem_failures = current_replicas * mem_failure_limit_per_pod
        sum_up_network_transmit_packets = current_replicas * network_transmit_packets_limit_per_pod
  
        if predicted_cpu > sum_up_requests * 0.7 or sum_up_mem_failures > predicted_memory_failures * 0.7 or sum_up_network_transmit_packets > predicted_network_transmit_packets * 0.7:
            # Calculate the new replica size  
            new_replica_size_from_cpu = math.ceil(predicted_cpu / cpu_limit_per_pod_milli) 
            new_replica_size_from_mem = math.ceil(predicted_memory_failures / mem_failure_limit_per_pod)
            new_replica_size_from_network = math.ceil(predicted_network_transmit_packets / network_transmit_packets_limit_per_pod)
            new_replica_size = max(new_replica_size_from_cpu, new_replica_size_from_mem, new_replica_size_from_network)
            if (new_replica_size <= current_replicas):
                print("[Warning] No need to scale in the deployment, predicted_cpu: ", predicted_cpu, ", sum_up_requests: ", sum_up_requests, ", predicted_memory_failures: ", predicted_memory_failures, ", sum_up_mem_failures: ", sum_up_mem_failures, ", predicted_network_transmit_packets: ",)
            else: 
                api_response.spec.replicas = new_replica_size  
                api_instance.patch_namespaced_deployment_scale(name=deployment, namespace=namespace, body=api_response)  
                if new_replica_size == new_replica_size_from_cpu:
                    print(f"Scale out deployment {deployment} to {api_response.spec.replicas} replicas. [Predicted CPU: {predicted_cpu}m, Current Limited CPU: {sum_up_requests}m={cpu_limit_per_pod_milli}m*{current_replicas}]")
                elif new_replica_size == new_replica_size_from_mem:
                    print(f"Scale out deployment {deployment} to {api_response.spec.replicas} replicas. [Predicted Memory Failures: {predicted_memory_failures}, Current Limited Memory Failures: {sum_up_mem_failures}={mem_failure_limit_per_pod}*{current_replicas}]")
                elif new_replica_size == new_replica_size_from_network:
                    print(f"Scale out deployment {deployment} to {api_response.spec.replicas} replicas. [Predicted Network Transmit Packets: {predicted_network_transmit_packets}, Current Limited Network Transmit Packets: {sum_up_network_transmit_packets}={network_transmit_packets_limit_per_pod}*{current_replicas}]")
        else:
            print("No need to scale the deployment")
  
    except ApiException as e:  
        print(f"Exception when calling AppsV1Api->read_namespaced_deployment: {e}")  
  
if __name__ == "__main__":  
    if len(sys.argv) != 4:  
        print(f"Usage: {sys.argv[0]} <namespace> <deployment> <predicted_cpu>")  
        sys.exit(1)  

    scale_deployment(sys.argv[1], sys.argv[2], float(sys.argv[3]))
