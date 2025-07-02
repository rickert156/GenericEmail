from module.manifest import domains_dir
import subprocess, os, sys

all_mode = ['run', 'start']

def helper():
    text = """\
    Пример использования:
    python3 startContainer.py run
    python3 startContainer.py start 
    """
    return text

def run_command(command:str):
    print(command)
    subprocess.run(command, shell=True)

def ListDirs():
    list_dirs = []
    for dirs in os.listdir(domains_dir):
        if 'base_' in dirs:
            path_dir = f"{domains_dir}/{dirs}"
            list_dirs.append(path_dir)

    return list_dirs

def selectMode():
    global all_mode
    params = sys.argv
    if len(params) > 1:
        mode = params[1]
        if mode in all_mode:
            return mode
        if mode not in all_mode:
            print(helper())
            sys.exit()
    else:
        print('Select MODE("run/start")')

def RunContainers():
    global all_mode
    list_dirs = ListDirs()

    main_cont_dir = '/GenericEmail/Domains'
    
    number_container = 0
    mode = selectMode()
    for target_dir in list_dirs:
        number_container+=1
        container = f"trustPilot_{number_container}"
        if mode == all_mode[0]:
            command = f"podman run -it -v $PWD/{target_dir}:{main_cont_dir} --name {container} generic &"
            run_command(command=command)
        if mode == all_mode[1]:
            command = f"podman start {container} &"
            run_command(command=command)

RunContainers()
