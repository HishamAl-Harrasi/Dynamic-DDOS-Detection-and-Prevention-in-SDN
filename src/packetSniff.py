#!/usr/bin/python3

from scapy.all import *        
from extractFeatures import *

class NetworkTraffic:
    def __init__(self, sniffTimeout = 5):
        self.sniffTimeout = sniffTimeout

        self.ipSrcAddresses = []
        self.ipDstAddresses = []
        self.packetCount = 0
        self.totalPacketSizes = 0

        # sniff(filter="ip", prn=self.parsePacketInfo, timeout=sniffTimeout)                                  # For normal machine testing & usage
        sniff(filter="ip", iface=["s1-eth1"], prn=self.parsePacketInfo, timeout=sniffTimeout)                 # For mininet testing & usage
        # sniff(filter="ip", iface=["s1-eth1", "s1-eth2"], prn=self.parsePacketInfo, timeout=sniffTimeout)    # For mininet testing & usage


    def parsePacketInfo(self, packet):
        # This is the callback function for the scapy.sniff() function, which stores the required data features for later analysis

        if IP in packet:
            self.ipSrcAddresses.append(packet[IP].src)
            self.ipDstAddresses.append(packet[IP].dst)
            self.totalPacketSizes += packet[IP].len
            self.packetCount += 1


    def getCapturedData(self):
        return [self.ipSrcAddresses, self.ipDstAddresses, self.packetCount, self.totalPacketSizes]


    def getDataFeatures(self, packetCapture, printStats=False):
        srcIPEntropy = calculateAverageEntropy(packetCapture[0], False)
        dstIPEntropy = calculateAverageEntropy(packetCapture[1], False)
        packetCount = packetCapture[2] if packetCapture[2] >= 1 else 1
        totalPacketSizes = packetCapture[3]

        avgPacketSize = totalPacketSizes / packetCount
        
        if printStats:
            print(f"Avg Source IP Entropy:      {srcIPEntropy}\nAvg Dest IP Entropy:        {dstIPEntropy}\nAvg Packet Size:            {avgPacketSize}\nTotal Packet Count:         {packetCount}\nPacket Arrival Rate:        {packetCount / self.sniffTimeout}\n\n")
        
        return [srcIPEntropy, dstIPEntropy, packetCount, avgPacketSize]


def sniffMininet():
    net = NetworkTraffic()
    packetCapture = net.getCapturedData()
    
    trafficFeatures = net.getDataFeatures(packetCapture, True)
    
    return trafficFeatures





