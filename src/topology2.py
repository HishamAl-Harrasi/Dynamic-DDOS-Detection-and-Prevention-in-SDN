import os
import sys

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch

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

# h1.setIP('172.24.0.1/16')
# h2.setIP('172.24.0.2/16')
# h3.setIP('172.24.0.3/16')
# h4.setIP('172.24.0.4/16')

print("\nNetwork topology created successfully! \n\n")
CLI(network)

network.stop()
