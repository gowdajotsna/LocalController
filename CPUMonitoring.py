from kubernetes import client, config
import time
class info:
    def __init__(self,cpu,mem):
        self.node_cpu=0
        self.pod_cpu=0


def convert_nanocores_to_millicores(cpu_nanocores_str):
    try:
        # Remove the 'n' from the string and convert to integer
        cpu_nanocores = int(cpu_nanocores_str.rstrip('n'))
        # Convert nanocores to millicores
        cpu_millicores = cpu_nanocores * 0.000001
        return cpu_millicores
    except ValueError:
        # Handle the case where conversion is not possible
        return 0.0  # or any other default value

# nodes
def printnodeinfo(k8s_nodes):
    cpuusage=[]
    for stats in k8s_nodes['items']:
        node_name = stats['metadata']['name']
        if node_name=='node1.reinierc-176345.ufl-eel6871-fa23-pg0.utah.cloudlab.us':
            cpu_nanocores_str = stats['usage']['cpu']
            cpu_millicores = convert_nanocores_to_millicores(cpu_nanocores_str)
            memory_usage = stats['usage']['memory']
            print(f"Node Name: {node_name}\tCPU: {cpu_millicores:.2f}m\tMemory: {memory_usage}")
            cpuusage.append(cpu_millicores)


    mean_cpu_usage = sum(cpuusage) / len(cpuusage) if len(cpuusage) > 0 else 0
    return mean_cpu_usage



# pods
def printpodsinfo(k8s_pods):
    for stats in k8s_pods['items']:
        namespace = stats['metadata']['namespace']
        if namespace == 'default':
            container_name = stats['containers'][0]['name']
            cpu_usage = stats['containers'][0]['usage']['cpu']
            cpu_usagem = convert_nanocores_to_millicores(cpu_usage)
            memory_usage = stats['containers'][0]['usage']['memory']
            metadata_name = stats['metadata']['name']

            # Print the information
            print(f"Container Name: {metadata_name}")
            print(f"CPU Usage: {cpu_usagem}")
            print(f"Memory Usage: {memory_usage}")


config.load_kube_config()

api = client.CustomObjectsApi()


def currentmonitor(duration_seconds=50):
    start_time = time.time()
    cpuusagenodes=[]
    while True:
        k8s_pods = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")
        printpodsinfo(k8s_pods)
        k8s_nodes = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
        cpuusagenodes.append(printnodeinfo(k8s_nodes))
        time.sleep(10)
    mean_cpu_usage = sum(cpuusagenodes) / len(cpuusagenodes) if len(cpuusagenodes) > 0 else 0
    return mean_cpu_usage

def currentPods():
    config.load_kube_config()

    # Create a CoreV1Api instance
    v1 = client.CoreV1Api()

    default_namespace_count = 0
    for pod in v1.list_pod_for_all_namespaces(watch=False).items:
        if pod.metadata.namespace == "default" and pod.status.phase == "Running":
            default_namespace_count += 1

    print(f"Number of pods in the 'default' namespace: {default_namespace_count}")
    return default_namespace_count