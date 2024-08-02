import subprocess
import json
import time
from kubernetes import client, config

def getNodeMetrics(nodeName):
    command = [
        "kubectl",
        "get",
        "--raw",
        f"/apis/metrics.k8s.io/v1beta1/nodes/{nodeName}"
    ]

    max_retries = 5
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            output = subprocess.check_output(command, text=True)
            metrics = json.loads(output)

            cpu_usage_raw = metrics.get('usage', {}).get('cpu')
            if cpu_usage_raw is None:
                print(f"CPU usage data not available. Attempt {attempt + 1} of {max_retries}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue

            last_character = cpu_usage_raw[-1]
            if last_character == 'n':
                cpu_usage = (float(cpu_usage_raw.rstrip('n')) * 0.0000001) / 16
            elif last_character == 'u':
                cpu_usage = (float(cpu_usage_raw.rstrip('u')) * 0.00001) / 16
            else:
                cpu_usage = 100.00 #Metrics server gets overloaded when too much cpu util and returns invalid raw

            print(f"CPU Usage: {cpu_usage}%")
            return cpu_usage

        except subprocess.CalledProcessError as e:
            print(f"\nCommand execution failed with error: {e}")
            time.sleep(retry_delay)

    print("\nFailed to retrieve CPU usage data after several attempts.")
    return -1

def getCurrentPodsCount(nodeName,namespace):
    config.load_kube_config()

    # Create a CoreV1Api instance
    v1 = client.CoreV1Api()

    namespace_count = 0
    for pod in v1.list_pod_for_all_namespaces(field_selector=f"spec.nodeName={nodeName}").items:
        if pod.metadata.namespace == namespace and pod.status.phase == "Running":
            namespace_count += 1

    print(f"Number of pods in the {namespace} namespace: {namespace_count}")

    return namespace_count



