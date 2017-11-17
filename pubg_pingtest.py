import psutil, re, subprocess, os, sys
import win32com.shell.shell as shell
from subprocess import check_output
from threading import Thread

def getAdminPermission():
    ASADMIN = 'asadmin'

    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        print ("Executing in root mode")

def getProcess(processName):
    for proc in psutil.process_iter():
        if proc.name() == processName:
            return proc

def extractIPfromString(string):
    return re.findall( r'[0-9]+(?:\.[0-9]+){3}', string )

def remove_duplicates(l):
    return list(set(l))

def pingOnConnections(p):
    conList = remove_duplicates(p.connections())

    for con in conList:
        ip = extractIPfromString(str(con.raddr))

        if not ip:
            continue

        if(ip[0] != "127.0.0.1" and ip[0] != ""):   #avoid local and empty requests
            print("Contacting " + str(ip))

            try:
                thread = Thread(target = pingSingleConnection, args = (ip, ))
                thread.start()
            except Exception:
                print("Cannot ping " + str(ip))
            
    print("Waiting for responses...\n")
    
def pingSingleConnection(arg):
    res = subprocess.Popen(["ping.exe", arg], stdout = subprocess.PIPE)
    time = str(res.communicate()[0]).split("Average = ")[1].split("ms")[0]
    print ("Average ping of " + str(arg[0]) + ": " + time + "ms\n")


p_name = "TslGame.exe"
p = None            #var host of the process

getAdminPermission()
p = getProcess(p_name)
if p:
    pingOnConnections(p)
else:
    print("No connection have been found")
