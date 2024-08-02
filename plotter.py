from matplotlib import pyplot as plot
# import backup as bk
import time
import stats
import states
import globalController
import argparse

node1_state_file = 'node1_state.json'
node2_state_file = 'node2_state.json'
global_state_file = 'global_state.json'

#Need Node 1 CPU
#Need Node 2 CPU
#or just overall Cluster CPU

#Specifcally Required in Spec:

    #Need Max Pods of each Node   - Can get from node json

    #Total Num Pods vs Time - Can alter node json to have cur pods field
        #Pods in Node 1 + Pods in Node 2

    #Total Number of Nodes in the Cluster - Can be determined, by if the node has pods
def calculate_active_nodes():
    active_nodes = 0

    if states.get_cur_pods_from_file(node1_state_file) > 0:
        active_nodes +=1
    if states.get_cur_pods_from_file(node2_state_file) > 0:
        active_nodes +=1

    return active_nodes

#Appends all values except time
def append_values():
    node1_max_pods.append(states.get_max_jobs_from_file(node1_state_file))
    node2_max_pods.append(states.get_max_jobs_from_file(node2_state_file))

    cur_total_pods = states.get_cur_pods_from_file(node1_state_file) + states.get_cur_pods_from_file(node2_state_file)
    total_pods.append(cur_total_pods)

    num_active_nodes.append(calculate_active_nodes())

    cluster_cpu_usage.append(states.get_cluster_cpu_from_file(global_state_file))

node1_max_pods = []
node2_max_pods = []
total_pods = []
num_active_nodes = []
cluster_cpu_usage = []
timeInSeconds = []

def collect_data(numJobsToRun):
     

    append_values()
    timeInSeconds.append(0)
    count = 1
    currently_done_job_count = states.get_currently_done_job_count_from_file(global_state_file)

    while currently_done_job_count < numJobsToRun - 1: ## as we know that the jobs.txt has 200 jobs
        
        time.sleep(15)

        append_values()
        timeInSeconds.append(count * 15)

        print("cpu_usage_list: " ,  cluster_cpu_usage[-1] )
        print("Node 1 Max Pods: " , node1_max_pods[-1] )
        print("Node 2 Max Pods: " , node2_max_pods[-1] )
        print("Total Pods: ",       total_pods[-1])
        print("Num Active Nodes: ", num_active_nodes[-1])
        
        currently_done_job_count = states.get_currently_done_job_count_from_file(global_state_file)
        count+=1

        
    print("Final Results:")
    print("cpu_usage_list: " ,  cluster_cpu_usage )
    print("Node 1 Max Pods: " , node1_max_pods )
    print("Node 2 Max Pods: " , node2_max_pods )
    print("Total Pods: ",       total_pods)
    print("Num Active Nodes: ", num_active_nodes)
    print("timeInSeconds_list: " ,  timeInSeconds )

    plotter(cluster_cpu_usage, node1_max_pods, node2_max_pods, total_pods, num_active_nodes, timeInSeconds)
    


def plotter(cluster_cpu_usage, node1_max_pods, node2_max_pods, total_pods, num_active_nodes, timeInSeconds):
    plot.figure(figsize=(10, 12))

    # Plot CPU Usages
    plot.subplot(5, 1, 1)
    plot.title('Cluster CPU % vs Time')
    plot.plot(timeInSeconds, cluster_cpu_usage, color="red", linestyle="-")
    plot.xlabel('Time (s)')
    plot.ylabel('CPU Usage (%)')

    # Plot Node 1 Max Pods
    plot.subplot(5, 1, 2)
    plot.title('Node 1 Max Pods vs Time')
    plot.plot(timeInSeconds, node1_max_pods, color="blue", linestyle="-")
    plot.xlabel('Time (s)')
    plot.ylabel('Max Pods')

    # Plot Node 2 Max Pods
    plot.subplot(5, 1, 3)
    plot.title('Node 2 Max Pods vs Time')
    plot.plot(timeInSeconds, node2_max_pods, color="green", linestyle="-")
    plot.xlabel('Time (s)')
    plot.ylabel('Max Pods')

    # Plot Total Pods
    plot.subplot(5, 1, 4)
    plot.title('Total Pods vs Time')
    plot.plot(timeInSeconds, total_pods, color="purple", linestyle="-")
    plot.xlabel('Time (s)')
    plot.ylabel('Total Pods')

    # Plot Number of Active Nodes
    plot.subplot(5, 1, 5)
    plot.title('Number of Active Nodes vs Time')
    plot.plot(timeInSeconds, num_active_nodes, color="orange", linestyle="-")
    plot.xlabel('Time (s)')
    plot.ylabel('Active Nodes')

    plot.tight_layout()
    plot.show()
    plot.savefig("graph.png")





#plotter(cluster_cpu_usage, node1_max_pods, node2_max_pods, total_pods, num_active_nodes, timeInSeconds)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Data Collector and Plotter")
    parser.add_argument("--num_jobs", type=int, default=74, help="Number of jobs to run (default: 74)")

    args = parser.parse_args()
    num_jobs = args.num_jobs

    collect_data(num_jobs)