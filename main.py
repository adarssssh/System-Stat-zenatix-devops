import psutil
import time
from elasticsearch import Elasticsearch
es = Elasticsearch()
#import json

def Process():

    listOfProcess = []

    # Iterate over the list
    for process in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = process.as_dict(attrs=['pid', 'name','cpu_percent'])
            pinfo['vms'] = process.memory_info().vms / (1024 * 1024)
            localtime = time.localtime(time.time())
            timestamp = int(localtime.tm_sec)
            pinfo['timestamp']=timestamp
            # Append dict to list
            listOfProcess.append(pinfo)
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Sort list of dict by key vms i.e. memory usage
        listOfProcess = sorted(listOfProcess, key=lambda procObj: procObj['vms'], reverse=True)

    return (listOfProcess)






if __name__ == "__main__":


    while True:
        listOfRunningProcess = Process()
        for elem in listOfRunningProcess:
            result = es.index(index="data-6", body=elem)
            #es.index(index="data",body=)
            print(result['result'])
            #Check the values
            #print(elem)
        #mem = psutil.virtual_memory()
    time.sleep(5)

