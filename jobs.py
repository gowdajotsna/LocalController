import argparse
import subprocess
import yaml
import time

filePath = "jobs.txt"
config_file = "kconfig.yaml"

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

def jobs(numOfPods, alreadyDoneJobs):
    with open(filePath) as f:
        lines = f.readlines()[alreadyDoneJobs:]
        jobs = lines[:numOfPods]
        if len(jobs) != numOfPods:
            print("No more jobs left/ took max jobs ... need to terminate")
            return 0
        jobs = [job.strip() for job in jobs]
        print(jobs)
        create_deployments(jobs, alreadyDoneJobs)


def create_deployments(stressng_commands, alreadyDoneJobs):

    # Load the original YAML file
    #with open(config_file, 'r') as file:
    #    original_config = yaml.safe_load(file)

    # Delete existing deployments
    #original_config.pop('deployments', None)
    count = alreadyDoneJobs + 1
    # Create a Deployment for each stress-ng command
    for i, stressng_command in enumerate(stressng_commands):

        deployment = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': f'stress-deployment-{count}',
            },
            'spec': {
                'restartPolicy':'Never',
                'containers': [
                            {
                                'name': 'stress-container',
                                'image': 'polinux/stress-ng:latest',
                                'args': stressng_command.split(),
                                'resources': {
                                    'requests': {
                                        'cpu': '500m'
                                    },
                                    'limits': {
                                        'cpu': '1000m'
                                    }
                                }
                            }
                        ],
                'nodeSelector': {
                    'kubernetes.io/hostname': 'node1.reinierc-176345.ufl-eel6871-fa23-pg0.utah.cloudlab.us'}
                    }
                }


        with open(f"kconfig_{count}.yaml", 'w') as file:
            yaml.dump(deployment,file, default_flow_style=False)
        # f = open(f"kconfig_{count}.yaml", "w")
        # f.write(str(deployment))
        # f.close()
        print(f"deployment{count}")
        count+=1
        #original_config.setdefault('deployments', []).append(deployment)
        time.sleep(15) ## to wait 15 s to take the next job
    apply_config(len(stressng_commands),alreadyDoneJobs)


def apply_config(numOfConfigs, alreadyDoneJobs):
    count = alreadyDoneJobs + 1

    for config in range(numOfConfigs):
        # Assuming kubectl is in your PATH
        kubectl_apply_command = f'kubectl apply -f kconfig_{count}.yaml'
        subprocess.run(kubectl_apply_command, shell=True)
        count+=1


    # # Save the modified YAML back to the file
    # with open(config_file, 'w') as file:
    #     yaml.dump(original_config, file, default_flow_style=False)


    # # Save the modified YAML back to the file
    # with open('/users/Group1/python/Jotsna/kconfig.yaml', 'w') as file:
    #     yaml.dump(original_config, file, default_flow_style=False)


#jobs(5,3)