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


