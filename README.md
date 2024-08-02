Kubernetes Cluster Controller
Overview
This project implements a Global Controller system for managing nodes within a Kubernetes cluster environment. The controller aims to optimize resource utilization by maintaining overall CPU usage below 80% while efficiently handling job allocation across nodes.
Features
Global Controller for managing total number of nodes
Local Controllers for determining MAX_PODS for each node
Periodic job queue processing (every 15 seconds)
Dynamic node addition and removal
Adaptive response to CPU utilization changes
Handling of node failures and workload fluctuations
Controller Design
The system uses a PID (Proportional-Integral-Derivative) controller for continuous closed-loop control. The chosen model for CPU utilization prediction is:
text
y(k+1) = -0.119 * y(k) + 0.105 * u(k)

Where:
y(k) is the CPU utilization at time k
u(k) is the control input at time k
Key Components
Global Controller: Manages overall cluster node count
Local Controllers: Determine MAX_PODS for individual nodes
Job Queue Reader: Processes jobs every 15 seconds
CPU Utilization Monitor: Tracks cluster-wide CPU usage
Implementation
The controller is implemented in Python and integrates with the Kubernetes API for cluster management.
Usage
[Include instructions on how to set up and run the controller]
Results
The controller successfully maintains CPU utilization around the target threshold (80%) by dynamically adjusting the number of nodes and pods in the cluster.
Contributors
Reinier Cruz Carnero
Anurag Chakraborty
Jotsna Gowda
Sumith Reddy Gutha
Darshini Ram Mattaparthi
