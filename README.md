# Kubernetes Cluster Controller

## Overview

This project implements a Global Controller system for managing nodes within a Kubernetes cluster environment. The controller's primary objective is to optimize resource utilization by ensuring overall CPU usage stays below 80%, while efficiently allocating jobs across nodes.

## Features

- **Global Controller:** Manages the total number of nodes in the cluster.
- **Local Controllers:** Determine MAX_PODS for each individual node based on resource availability.
- **Periodic Job Queue Processing:** Jobs are processed every 15 seconds to maintain efficient workload distribution.
- **Dynamic Node Management:** Supports dynamic addition and removal of nodes based on workload and resource demands.
- **Adaptive CPU Utilization:** Utilizes a PID (Proportional-Integral-Derivative) controller model for adaptive response to CPU utilization changes.
- **Fault Tolerance:** Handles node failures and workload fluctuations gracefully.

## Controller Design

The system employs a PID controller for continuous closed-loop control of CPU utilization. y(k+1) = -0.119 * y(k) + 0.105 * u(k)
Where:
- `y(k)`: CPU utilization at time k.
- `u(k)`: Control input at time k.

## Key Components

- **Global Controller:** Manages overall cluster node count.
- **Local Controllers:** Calculate and enforce MAX_PODS for individual nodes.
- **Job Queue Reader:** Processes job queues every 15 seconds.
- **CPU Utilization Monitor:** Tracks cluster-wide CPU usage.

## Implementation

The controller is implemented in Python and integrates with the Kubernetes API for seamless cluster management. In our case we implemented the entire scenario in CloudLab.

## How to execute:
1) Execute the makefile to install all the necessary libraries:
  	 Use the command `sudo make`
2) Run the python file globalController.py:
Use the command `sudo python globalController.py`
3) Set the amount of jobs to record in plotter.py while running the file on command-line.
	Use the command `sudo python ./plotter.py --num_jobs <NUMBER_OF_JOBS>`
4) NOTE: If running multiple times
   - to delete previous run's pods use command `sudo ./delete_pods.sh`. This script will delete all pods in all namespaces.
   - to delete previous run's config.yaml files use command `sudo ./delete_kconfig.sh`. This script will delete all config files generated from previous runs.

## Our project includes the following files:
1. globalController.py
2. Jobs.py
3. localController.py
4. manipulate_cluster.py
5. Plotter.py
6. states.py
7. Stats.py
8. jobs.txt
 
 
**globalController.py:**

This Python script functions as a global controller for managing job scheduling in a Kubernetes cluster. It leverages the Kubernetes Python client library to interact with the cluster API. The script maintains state information in JSON files, including cluster-wide CPU utilization, the number of completed jobs globally, and the maximum allowable job count for each node. The script employs PID controllers to dynamically adjust the maximum pod count for each node based on its CPU utilization. The main loop continuously evaluates conditions for scheduling new jobs on nodes, considering factors such as the current pod count, maximum pod count, and global job completion count. It also monitors node and cluster metrics, adjusting parameters as needed. In the event of no more jobs to schedule, the script waits for all existing pods to finish while periodically updating metrics. The script is designed to run until all jobs are completed, ensures efficient use of resources and effective management of the Kubernetes cluster.
 
**Jobs.py:**

This Python script is a job scheduler for a Kubernetes cluster and acts as a middleware, designed to deploy stress-ng workloads on specified nodes. The script reads job configurations from a file `jobs.txt` and deploys stress-ng workloads as Kubernetes Pods on either `node1` or `node2` based on the defined nodes and namespaces. The script dynamically generates YAML configuration files for each stress-ng command, creating a new deployment for each workload. It utilizes the Kubernetes Python client library to apply these configurations, deploying Pods with stress-ng containers to stress-test the specified nodes. The jobs function manages the scheduling of these stress-ng workloads, determining if there are still jobs remaining to be deployed. The create_deployments function generates YAML configurations for stress-ng deployments and writes them to files, while the apply_config function uses kubectl apply to deploy the configurations to the Kubernetes cluster. 

**localController.py:**

This Python code defines a simple Proportional-Integral-Derivative (PID) controller class. PID controllers are widely used in control systems to maintain a system at a desired setpoint by adjusting a control input based on the error, integral of error, and derivative of error. In this implementation, the PID class has three coefficients: proportional gain (kp), integral gain (ki), and derivative gain (kd). The calculate_control_input method takes a measured value as input, computes the error, and updates the control input based on the PID equation. The control input is then returned. The sumerr variable accumulates the integral of the error over time, preverr stores the previous error for derivative computation, and derr represents the derivative of the error. The code includes a sample usage of the PID controller by creating an instance and calling the calculate_control_input method with a measured value of 0.6. 

**manipulate_cluster.py**

This Python script provides a set of functions for managing nodes in a Kubernetes cluster. The un_cordon_node function unmarks a node as unschedulable, allowing it to receive new pods. Conversely, the cordon_node function marks a node as unschedulable, preventing new pods from being assigned to it. The evict_pods_from_node function selectively evicts pods from a specified node, excluding those belonging to DaemonSets, which are critical system pods.

***Technical Info:***

***un_cordon_node(node_name):*** This function uses the Kubernetes API to unmark a node as unschedulable. It loads the Kubernetes configuration, creates an API client for accessing the CoreV1 API, and sends a patch request to the specified node, updating its unschedulable attribute to False.

***cordon_node(node_name):*** Similar to the previous function, this one marks a node as unschedulable by sending a patch request with the unschedulable attribute set to True. This is useful when a node is under maintenance or experiencing issues, and new workloads should not be scheduled on it.

***evict_pods_from_node(node_name, namespace):*** This function evicts pods from the specified node, excluding those associated with DaemonSets. It lists all pods on the given node in the specified namespace, skips DaemonSet pods during iteration, and proceeds to evict the remaining pods using the Kubernetes eviction API. It prints relevant information about each evicted pods.

**Plotter.py**

This Python script performs real-time monitoring and data collection of a Kubernetes cluster's performance metrics and workload distribution. It takes in the number of jobs to record the command line to collect data for. The collect_data function continuously appends various metrics, such as CPU usage, maximum pods for each node, total pods, and the number of active nodes, to respective lists. The script simulates a cluster environment by adjusting the number of active nodes and running jobs at intervals. The plotter function utilizes the Matplotlib library to create a multi-subplot graph, visualizing the time-series data for each metric. The resulting graphs provide insights into the cluster's behavior, showcases how it adapts to changing workloads and node configurations over time.

**States.py**

This python script basically writes the #max_jobs and #number of currently completed jobs, #number of current pods, #cluster cpu%  in the .json file for plotting purpose.

**Stats.py**

This Python script retrieves metrics related to CPU usage and the count of running pods on a specified Kubernetes node. The getNodeMetrics function uses the kubectl command-line tool to query the Kubernetes API for node-level metrics, to get CPU usage. The function handles  inconsistencies in the metric data format and converts the raw values to a percentage value. The getCurrentPodsCount function utilizes the Kubernetes Python client library to count the number of running pods on a given node within a specified namespace. It uses a subprocess for executing kubectl commands, the Kubernetes Python client library for querying pod information.

**Jobs.txt:**

This has a list of jobs or stressors with varying `io` and `vm`.

