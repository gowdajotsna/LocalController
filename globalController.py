import stats #gets cur pods and node cpu utilization
import states #Manipulates json files
import jobs
import time
import localController
from kubernetes import client, config

def main():
    #######################################################################
    node1 = "node1.reinierc-176345.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
    node1_state_file = 'node1_state.json'
    node1_namespace = "node1-namespace"

    node2 = "node2.reinierc-176345.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
    node2_state_file = 'node2_state.json'
    node2_namespace = "node2-namespace"

    global_state_file = 'global_state.json'

    node1_max_pods = 8
    node2_max_pods = 5 


    global_currently_done_jobs = 0

    cur_done_jobs_node1=0
    cur_done_jobs_node2=0

    cluster_cpu = 0.0
    isMoreJobs = True
    isJobsCompleted=False
    isNode2Active = False
    node1AllowedToRun = True
    node2AllowedToRun = True
    #######################################################################

    node1_controller = localController.PID()
    node2_controller = localController.PID()

    #Initalize Nodes to be Able to Run
    states.write_node_allowed_to_run_to_file(node1AllowedToRun, node1_state_file)
    states.write_node_allowed_to_run_to_file(node2AllowedToRun, node2_state_file)

    #Intalize global json
    states.write_cluster_cpu_to_file(0, global_state_file)
    states.write_currently_done_job_count_to_file(0, global_state_file)

    #Need to write max pods to respective json files
    states.write_max_jobs_to_file(node1_max_pods, node1_state_file)
    states.write_max_jobs_to_file(node2_max_pods, node2_state_file)

    #Clear out previously done jobs
    states.write_cur_pods_to_file(0, node1_state_file)
    states.write_cur_pods_to_file(0, node2_state_file)

    #Using local variables instead of class variables for now, feel free to make into a class
    node1_cpu = stats.getNodeMetrics(node1)
    node1_cur_pods = stats.getCurrentPodsCount(node1,node1_namespace)
    node1_max_pods = states.get_max_jobs_from_file(node1_state_file)

    node2_cpu = stats.getNodeMetrics(node2)
    node2_cur_pods = stats.getCurrentPodsCount(node2,node2_namespace)
    node2_max_pods = states.get_max_jobs_from_file(node2_state_file)

    print(f"Node1 Inital Current Pods: {node1_cur_pods}")
    print(f"Node2 Inital Current Pods: {node2_cur_pods}")

    while not isJobsCompleted:

        print(f"Node1 Max Pods: {node1_max_pods}")
        print(f"Node2 Max Pods: {node2_max_pods}")
        print(f"Globally Done Jobs: {global_currently_done_jobs}")

        node1AllowedToRun = states.get_node_allowed_to_run_from_file(node1_state_file)
        node2AllowedToRun = states.get_node_allowed_to_run_from_file(node2_state_file)
        
        if (node1_cur_pods < node1_max_pods and (cluster_cpu <= 80.0 or not node2AllowedToRun)) and node1AllowedToRun:
            numJobsToRun = node1_max_pods - node1_cur_pods
            isMoreJobs = jobs.jobs(global_currently_done_jobs, numJobsToRun, node1)
            global_currently_done_jobs += numJobsToRun
            print(f"Node 1 changed global done jobs to: {global_currently_done_jobs}")

        elif ((node2_cur_pods < node2_max_pods and (cluster_cpu >= 80.0 or not node1AllowedToRun))) and node2AllowedToRun:
            isNode2Active = True
            numJobsToRun = node2_max_pods - node2_cur_pods
            isMoreJobs = jobs.jobs(global_currently_done_jobs, numJobsToRun, node2)
            global_currently_done_jobs += numJobsToRun
            print(f"Node 2 changed global done jobs to: {global_currently_done_jobs}")
            #states.write_currently_done_job_count_to_file(cur_done_jobs_node2, node2_state_file)


        if isMoreJobs == False:
            print("\n\n ---- no more jobs ----- \n\n")
            isJobsCompleted = True
            continue

        time.sleep(15)

        #Node 1 Calculations
        node1_cpu = stats.getNodeMetrics(node1)
        node1_cur_pods = stats.getCurrentPodsCount(node1, node1_namespace)
        if node1AllowedToRun:
            node1_max_pods = round(node1_controller.calculate_control_input(node1_cpu/100))
            states.write_max_jobs_to_file(node1_max_pods, node1_state_file)
    
        #Node 2 Calculations
        node2_cpu = stats.getNodeMetrics(node2)
        node2_cur_pods = stats.getCurrentPodsCount(node2, node2_namespace)
        #Don't want to increase controller error when the node is not active
        if node2AllowedToRun and isNode2Active:
            node2_max_pods =  round(node2_controller.calculate_control_input(node2_cpu/100))
            states.write_max_jobs_to_file(node2_max_pods, node2_state_file)

        
        states.write_cur_pods_to_file(node1_cur_pods, node1_state_file)
        states.write_cur_pods_to_file(node2_cur_pods, node2_state_file)


        if node2_cur_pods > 0 and node1_cur_pods > 0:
            print("Calculating Cluster CPU from both nodes")
            cluster_cpu=(node1_cpu + node2_cpu) / 2
        elif node2_cur_pods == 0 and node1_cur_pods > 0:
            print("Calculating Cluster CPU from Node 1")
            cluster_cpu = node1_cpu
        elif node1_cur_pods == 0 and node2_cur_pods > 0:
            print("Calculating Cluster CPU from Node 2")
            cluster_cpu = node2_cpu

        states.write_cluster_cpu_to_file(cluster_cpu, global_state_file)
        states.write_currently_done_job_count_to_file(global_currently_done_jobs, global_state_file)


    ## NO MORE JOBS, exited while loop, add case to check cpu for running jobs in node 1 and node 2#####
    while node1_cur_pods >= 1 or node2_cur_pods >= 1:
        print("Waiting for all pods to finish...\n")

        node1_cur_pods = stats.getCurrentPodsCount(node1, node1_namespace)
        node2_cur_pods = stats.getCurrentPodsCount(node2, node2_namespace)
        states.write_cur_pods_to_file(node1_cur_pods, node1_state_file)
        states.write_cur_pods_to_file(node2_cur_pods, node2_state_file)
        
        node1_cpu = stats.getNodeMetrics(node1)
        node2_cpu = stats.getNodeMetrics(node2)

        if node2_cur_pods > 0 and node1_cur_pods > 0:
            print("Calculating Cluster CPU from both nodes")
            cluster_cpu=(node1_cpu + node2_cpu) / 2
        elif node2_cur_pods == 0 and node1_cur_pods > 0:
            print("Calculating Cluster CPU from Node 1")
            cluster_cpu = node1_cpu
        elif node1_cur_pods == 0 and node2_cur_pods > 0:
            print("Calculating Cluster CPU from Node 2")
            cluster_cpu = node2_cpu

        states.write_cluster_cpu_to_file(cluster_cpu, global_state_file)

        time.sleep(5)


    print("\n\n--------globalController Finished--------\n\n")


if __name__ == '__main__':
    main()
