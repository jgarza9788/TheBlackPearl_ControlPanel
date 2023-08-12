

import subprocess

def run_cmd(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def is_running(programs:list,verbose=False):
    rc = run_cmd("tasklist")

    rc = str(rc.stdout.read())

    if verbose:
        print(rc)
    
    result = []
    for p in programs:
        if p in rc:
            result.append({"name":p,"on":True})
        else:
            result.append({"name":p,"on":False})
    
    return result




if __name__ == "__main__":
    
    ir = is_running(
        [
            'NordVPN.exe',
            'Plex Media Server.exe',
            'qbittorrent.exe',
            'Code.exe'
        ],True)
    print(ir)