import argparse
import subprocess
import yaml
import time

filePath = "jobs.txt"
config_file = "kconfig.yaml"
node1 = "node1.reinierc-176345.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
node1_namespace = "node1-namespace"
node2 = "node2.reinierc-176345.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
node2_namespace = "node2-namespace"

# stress-ng
# --io
#  1
#  --vm
#  1
#  --vm-bytes
#  1G
#  --timeout
#  2m
# stress-ng --io 2 --vm 1 --vm-bytes 1G --timeout 2m
""" def get_stressors(jobList):
    for job in jobList:
        create_deployments() """
#Returns true if there are still jobs
#False if no more jobs
def jobs(alreadyDoneJobs, numOfPodsRequested, nodeName):
    print(f"Already done jobs: {alreadyDoneJobs}")

    with open(filePath) as f:
        lines = f.readlines()[alreadyDoneJobs:]
        jobsRemainingCount = len(lines)
        if (jobsRemainingCount -  numOfPodsRequested) > 0: ## base case, when we have more jobs in queue
            jobsRemaining = lines[:numOfPodsRequested]
            jobs = [job.strip() for job in jobsRemaining]
            print(jobs)
            create_deployments(jobs, alreadyDoneJobs,nodeName)
            return True
        elif ((jobsRemainingCount -  numOfPodsRequested) == 0): ## case when requested jobs and the num of jobs in queue are exact match, deploy all and terminate as no more jobs left
            jobsRemaining = lines[:numOfPodsRequested]
            jobs = [job.strip() for job in jobsRemaining]
            print(jobs)
            print("took exact match of jobs left")
            create_deployments(jobs, alreadyDoneJobs,nodeName)
            return False
        elif ((jobsRemainingCount - numOfPodsRequested) < 0):## case when requested jobs are greater than the number of jobs left, deploy remaining and terminate
            jobsRemaining = lines[:numOfPodsRequested]
            print("took all remaining jobs... need to terminate")
            jobs = [job.strip() for job in jobsRemaining ]
            print(jobs)
            create_deployments(jobs, alreadyDoneJobs,nodeName)
            return False

def create_deployments(stressng_commands, alreadyDoneJobs, nodeName):
    count = alreadyDoneJobs + 1

    if nodeName == node1:
        namespace = node1_namespace
        curNode = "node1"
    elif nodeName == node2:
        namespace = node2_namespace
        curNode = "node2"
    else:
        print("\n\n\n Mismatch with node names in jobs.py \n\n\n")

    print(f"Creating deployment for {curNode}")

    # Create a Deployment for each stress-ng command
    for i, stressng_command in enumerate(stressng_commands):
        deployment = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': f'stress-deployment-{count}',
                'namespace': f'{namespace}',
            },
            'spec': {
                'restartPolicy':'Never',
                'containers': [
                            {
                                'name': f'stress-container-{count}',
                                'image': 'polinux/stress-ng:latest',
                                'imagePullPolicy': 'IfNotPresent',
                                'args': stressng_command.split(),
                                'resources': {
                                    'requests': {
                                        'cpu': '250m'
                                    },
                                    'limits': {
                                        'cpu': '3000m'
                                    }
                                }
                            }
                        ],
                'nodeSelector': {
                    'kubernetes.io/hostname': f'{nodeName}'}
                    }
                }

        #To prevent possible error of config getting rewritten, added node to name


        with open(f"kconfig_{count}_{curNode}.yaml", 'w') as file:
            yaml.dump(deployment, file, default_flow_style=False)

        print(f"deployment{count}")
        count+=1

    apply_config(len(stressng_commands), alreadyDoneJobs, curNode)


def apply_config(numOfConfigs, alreadyDoneJobs, curNode):
    count = alreadyDoneJobs + 1

    for config in range(numOfConfigs):
        # Assuming kubectl is in your PATH
        kubectl_apply_command = f'kubectl apply -f kconfig_{count}_{curNode}.yaml'
        subprocess.run(kubectl_apply_command, shell=True)
        count+=1


#jobs(10,11)
