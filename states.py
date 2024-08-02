import json


#################################################################################
def write_node_allowed_to_run_to_file(boolTF, state_file):
    state = read_state_from_file(state_file)
    state['node_allowed_to_run'] = boolTF
    write_state_to_file(state, state_file)

def get_node_allowed_to_run_from_file(state_file):
    state = read_state_from_file(state_file)
    return state.get('node_allowed_to_run', -1)  # default to -1 if not found
#################################################################################

#################################################################################
def write_cur_pods_to_file(count, state_file):
    state = read_state_from_file(state_file)
    state['cur_pods_count'] = count
    write_state_to_file(state, state_file)

def get_cur_pods_from_file(state_file):
    state = read_state_from_file(state_file)
    return state.get('cur_pods_count', -1)  # default to -1 if not found
#################################################################################

def write_currently_done_job_count_to_file(count, state_file):
    """Writes the currently done job count to a file."""
    state = read_state_from_file(state_file)
    state['currently_done_job_count'] = count
    write_state_to_file(state, state_file)

def write_max_jobs_to_file(max_jobs, state_file):
    """Writes the max jobs to a file."""
    state = read_state_from_file(state_file)
    state['max_jobs'] = max_jobs
    write_state_to_file(state, state_file)

#################################################################################
def write_cluster_cpu_to_file(cpu_usage, state_file):
    state = read_state_from_file(state_file)
    state['cluster_cpu'] = cpu_usage
    write_state_to_file(state, state_file)

def get_cluster_cpu_from_file(state_file):
    state = read_state_from_file(state_file)
    return state.get('cluster_cpu', -1)
#################################################################################


def get_currently_done_job_count_from_file(state_file):
    """Returns the currently done job count from the file."""
    state = read_state_from_file(state_file)
    return state.get('currently_done_job_count', -1)  # default to 0 if not found

def get_max_jobs_from_file(state_file):
    """Returns the max jobs from the file."""
    state = read_state_from_file(state_file)
    return state.get('max_jobs', -1)  # default to -1 if not found





#################################################################################
def read_state_from_file(state_file):
    """Reads the state from the file and returns it."""
    try:
        with open(state_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading from file")
        return {}  

def write_state_to_file(state, state_file):
    """Writes the entire state to a file."""
    try:
        with open(state_file, 'w') as file:
            json.dump(state, file)
    except Exception as e:
        print(f"Error writing to file: {e}")
#################################################################################