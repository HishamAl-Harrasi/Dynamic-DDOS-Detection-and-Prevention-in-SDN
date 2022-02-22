#/usr/bin/python3

import os
import sys
import time
from threading import Thread
import threading

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch

from generateNormalTraffic import *
from generateDDOSTraffic import *


PCAP_MODE = False
GENERATE_NORMAL_TRAFFIC = True
GENERATE_DDOS_TRAFFIC = False
GENERATE_NORMAL_AND_DDOS_TRAFFIC = False
CLEAN_STARTUP = False


if os.geteuid() != 0:
    sys.exit("\nError. Programs needs to be run as root.\n")

network = Mininet()

h1 = network.addHost('h1')
h2 = network.addHost('h2')
h3 = network.addHost('h3')
h4 = network.addHost('h4')

h5 = network.addHost('h5')
h6 = network.addHost('h6')
h7 = network.addHost('h7')
h8 = network.addHost('h8')

s1 = network.addSwitch('s1')
s2 = network.addSwitch('s2')
#s1 = network.addSwitch('s1', cls=OVSKernelSwitch, protocols='OpenFlow13')
#s2 = network.addSwitch('s2', cls=OVSKernelSwitch, protocols='OpenFlow13')

c1 = network.addController('c0')

network.addLink(h1, s1)
network.addLink(h2, s1)
network.addLink(h3, s1)
network.addLink(h4, s1)

network.addLink(h5, s2)
network.addLink(h6, s2)
network.addLink(h7, s2)
network.addLink(h8, s2)

network.addLink(s1, s2)


network.start()

# Disallow ipv6 connections - they tamper with tcpdump's packet captures so a decision was made to remove them
# Reference: https://gist.github.com/tudang/87da66215116e2ba5afd250a9fb8a9c8
for h in network.hosts:
    h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
    h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
    h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")

for sw in network.switches:
    sw.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
    sw.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
    sw.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")


print("\nNetwork topology created successfully!\n")

# Make each hosts shell accessible from within this python script
h1, h2, h3, h4, h5, h6, h7, h8 = network.get("h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8")
s1, s2 = network.get("s1", "s2")
c0 = network.get("c0")


print("\nGenerating and capturing traffic.. \n\n")

mergeCommandS1 = "mergecap -w merged1.pcap "
cleanupCommandS1 = "rm -f "
mergeCommandS2 = "mergecap -w merged2.pcap "
cleanupCommandS2 = "rm -f "

if PCAP_MODE:
    for i, intf in enumerate(s1.intfNames()):
        if intf != "lo":
            s1.cmd(f"tcpdump -s0 -i {intf} -w ./packetCaptureS1-{i}.pcap &")
            mergeCommandS1 += f"packetCaptureS1-{i}.pcap "
            cleanupCommandS1 += f"packetCaptureS1-{i}.pcap "

    for i, intf in enumerate(s2.intfNames()):
        if intf != "lo":
            s2.cmd(f"tcpdump -s0 -i {intf} -w ./packetCaptureS2-{i}.pcap &")
            mergeCommandS2 += f"packetCaptureS2-{i}.pcap "
            cleanupCommandS2 += f"packetCaptureS2-{i}.pcap "

if GENERATE_NORMAL_TRAFFIC:

    t1 = Thread(target=loopGNT, args=(h1, h2.IP()))
    t2 = Thread(target=loopGNT, args=(h3, h4.IP()))
    t3 = Thread(target=loopGNT, args=(h5, h6.IP()))
    t4 = Thread(target=loopGNT, args=(h7, h8.IP()))

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t4.daemon = True


    time.sleep(1)
    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(1)
    t3.start()
    time.sleep(1)
    t4.start()

    CLI(network)

    t1.join()
    t2.join()
    t3.join()
    t4.join()

elif GENERATE_DDOS_TRAFFIC:
    t1 = Thread(target=loopGDT, args=(h1, h2.IP()))
    t1.daemon = True
    time.sleep(1)
    t1.start()

    CLI(network)

    t1.join()

elif GENERATE_NORMAL_AND_DDOS_TRAFFIC:

    t1 = Thread(target=loopGNT, args=(h1, h5.IP()))   # Normal Traffic
    t2 = Thread(target=loopGNT, args=(h2, h6.IP()))   # Normal Traffic
    t3 = Thread(target=loopGNT, args=(h3, h7.IP()))   # Normal Traffic
    t4 = Thread(target=loopGNT, args=(h4, h8.IP()))   # Normal Traffic
    
    t5 = Thread(target=loopGDTSS, args=(h5, h2.IP()))   # DDOS Traffic - This could be loopGDT or loopGDTSS

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t4.daemon = True

    t5.daemon = True

    time.sleep(1)
    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(1)
    t3.start()
    time.sleep(1)
    t4.start()

    time.sleep(1)
    t5.start()

    CLI(network)

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    t5.join()


elif CLEAN_STARTUP:
    CLI(network)


# Exit and mininet cleanup
print("\n\n\tExiting and cleaning mininet..\n\n\n")
network.stop()
os.system("mn -c > /dev/null 2>&1")

if PCAP_MODE:
    os.system(mergeCommandS1)
    os.system(mergeCommandS2)
    os.system(cleanupCommandS1)
    os.system(cleanupCommandS2)



        
