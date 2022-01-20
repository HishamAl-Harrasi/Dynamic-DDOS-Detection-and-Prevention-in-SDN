#!/usr/bin/python3

from scapy.all import *        


class NetworkTraffic:
    def __init__(self, sniffTimeout = 5):
        self.ipSrcAddresses = []
        self.ipDstAddresses = []
        self.packetCount = 0
        self.totalPacketLengths = 0

        # sniff(filter="ip", prn=self.parsePacketInfo, timeout=sniffTimeout)                                  # For normal machine testing & usage
        sniff(filter="ip", iface=["s1-eth1"], prn=self.parsePacketInfo, timeout=sniffTimeout)                 # For mininet testing & usage
        # sniff(filter="ip", iface=["s1-eth1", "s1-eth2"], prn=self.parsePacketInfo, timeout=sniffTimeout)    # For mininet testing & usage


    def parsePacketInfo(self, packet):
        # This is the callback function for the scapy.sniff() function, which stores the required data features for later analysis

        if IP in packet:
            self.ipSrcAddresses.append(packet[IP].src)
            self.ipDstAddresses.append(packet[IP].dst)
            self.totalPacketLengths += packet[IP].len
            self.packetCount += 1


    def getCapturedData(self):
        return [self.ipSrcAddresses, self.ipDstAddresses, self.packetCount, self.totalPacketLengths]


def sniffMininet():
    net = NetworkTraffic()
    dataCapture = net.getCapturedData()
    
    return dataCapture





