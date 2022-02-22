import random
import os
import sys
import time

from mininet.net import Mininet

def generateNormalTraffic(targetIP):
    rand = random.choice([1, 2, 3])
    
    if rand == 1:
        # os.system(f"nping --tcp -c 5 {targetIP} -q > /dev/null 2>&1 &")
        return f"nping --tcp -c 5 {targetIP} -q > /dev/null 2>&1 &"
    elif rand == 2:
        # os.system(f"nping --udp -c 5 {targetIP} -q > /dev/null 2>&1 &")
        return f"nping --udp -c 5 {targetIP} -q > /dev/null 2>&1 &"
    else:
        # os.system(f"nping --icmp -c 5 {targetIP} -q > /dev/null 2>&1 &")
        return f"nping --icmp -c 5 {targetIP} -q > /dev/null 2>&1 &"



def loopGNT(hostObj, targetIP): # Loop through generateNormalTraffic function
    i = 0
    while i < 10000:
        cmd = generateNormalTraffic(targetIP)
        hostObj.cmd(cmd) # This does not wait for the command to complete
        time.sleep(4.5)
        i += 1
        




if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("\nError. Programs needs to be run as root.\n")

    target = sys.argv[1:]

    generateNormalTraffic(target)
    