#controller will call monitor function and pass maxjobs as argument
import CPUMonitoring
import jobs
#import controller
currently_done_job_count = 0
max_jobs = 2
def monitor(max_jobs):
    current_pods=CPUMonitoring.currentPods()
    print(current_pods )
    global currently_done_job_count
    currently_done_job_count+=current_pods
    if max_jobs>current_pods:
        print("inside condition")
        no_of_pods=max_jobs - current_pods
        print("num of pods : " + str(no_of_pods))
        value = jobs.jobs(no_of_pods, currently_done_job_count)
        if(value == 0):
            print("terminate")
            exit()
    cpuutil=CPUMonitoring.currentmonitor()
    print(cpuutil)
    #max_jobs=controller(cpuutil)

monitor(max_jobs)