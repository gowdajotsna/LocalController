import argparse
from kubernetes import client, config
import states

node1 = "node1.reinierc-176345.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
node2 = "node2.reinierc-176345.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
node1_namespace = "node1-namespace"
node2_namespace = "node2-namespace"

node1_state_file = 'node1_state.json'
node2_state_file = 'node2_state.json'


def un_cordon_node(node_name):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = {
        "spec": {
            "unschedulable": False
        }
    }
    v1.patch_node(node_name, body)

    if node_name == node1:
        states.write_node_allowed_to_run_to_file(True, node1_state_file)
    elif node_name == node2:
        states.write_node_allowed_to_run_to_file(True, node2_state_file)
    else:
        print("Error with node name in manipulate_cluster.py")

    print(f"Node {node_name} uncordoned.")

#logic to cordon,drain and uncordon a node-basically killing a node
#we should kill a node when it reaches 80% utlization
def cordon_node(node_name):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = {
        "spec": {
            "unschedulable": True
        }
    }
    v1.patch_node(node_name, body)

    if node_name == node1:
        states.write_node_allowed_to_run_to_file(False, node1_state_file)
    elif node_name == node2:
        states.write_node_allowed_to_run_to_file(False, node2_state_file)
    else:
        print("Error with node name in manipulate_cluster.py")

    print(f"Node {node_name} cordoned.")

def evict_pods_in_namespace(namespace):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    # List all pods in the specified namespace, excluding DaemonSets
    pods = v1.list_namespaced_pod(namespace=namespace).items

    for pod in pods:
           # Evict the pod
        try:
            eviction = client.V1Eviction(
                metadata=client.V1ObjectMeta(name=pod.metadata.name, namespace=namespace))
            v1.create_namespaced_pod_eviction(name=pod.metadata.name, namespace=namespace, body=eviction)
            print(f"Pod {pod.metadata.name} in namespace {namespace} evicted.")
        except client.rest.ApiException as e:
            print(f"Exception when evicting pod {pod.metadata.name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kubernetes Node Management Script")
    parser.add_argument("action", choices=['cordon', 'uncordon', 'evict', 'cordon_and_evict'], help="Action to perform (cordon, uncordon, evict, or cordon_and_evict)")
    parser.add_argument("node", help="Node identifier (node1 or node2)")

    args = parser.parse_args()

    nodes = {
        "node1": {"name": node1, "namespace": node1_namespace},
        "node2": {"name": node2, "namespace": node2_namespace}
    }

    node_name = nodes[args.node]["name"]
    namespace = nodes[args.node]["namespace"]

    if args.action == "cordon":
        cordon_node(node_name)
    elif args.action == "uncordon":
        un_cordon_node(node_name)
    elif args.action == "evict":
        evict_pods_in_namespace(namespace)
    elif args.action == "cordon_and_evict":
        # Cordon the node first
        cordon_node(node_name)
        # Then evict the pods in the node's namespace
        evict_pods_in_namespace(namespace)

