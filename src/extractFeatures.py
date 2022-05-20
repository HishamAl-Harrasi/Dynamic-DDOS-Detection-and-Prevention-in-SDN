#!/usr/bin/python3

import numpy as np
import pandas as pd
import collections


def extractIP(packetCapture):  # Extract the IP address from the packet capture
    ipAddresses = []

    for ip in packetCapture["ip.src"]:
        if type(ip) == str:
            ipAddresses.append(ip)

    return ipAddresses


def splitIP(ipAddresses):  # Split IP Address into its 4 octets
    srcAddrSplit = []
    for ip in ipAddresses:
        srcAddrSplit.append(ip.split("."))

    firstOctet, secondOctet, thirdOctet, fourthOctet = [], [], [], []
    for i in srcAddrSplit:
        firstOctet.append(i[0])
        secondOctet.append(i[1])
        thirdOctet.append(i[2])
        fourthOctet.append(i[3])

    return [firstOctet, secondOctet, thirdOctet, fourthOctet]


def countIPOcurrances(ipOctets):  # Count the occurances of each number in each octet
    firstOctetOccurances = collections.Counter(ipOctets[0])
    secondOctetOccurances = collections.Counter(ipOctets[1])
    thirdOctetOccurances = collections.Counter(ipOctets[2])
    fourthOctetOccurances = collections.Counter(ipOctets[3])

    return [firstOctetOccurances, secondOctetOccurances, thirdOctetOccurances, fourthOctetOccurances]


# Use shannon entropy to calculate the randomness of IP addresses
def calculateAverageEntropy(srcIPAddresses, printInfo=False):
    # Reference: https://stackoverflow.com/questions/27432078/entropy-of-ip-packet-information?rq=1
    srcIPAddrSplit = splitIP(srcIPAddresses)
    octets = countIPOcurrances(srcIPAddrSplit)

    totalEntropy = 0

    for i, octet in enumerate(octets):
        counts = np.array(list(octet.values()))
        probability = counts / counts.sum()
        shannonEntropy = (-probability * np.log2(probability)).sum()
        totalEntropy += shannonEntropy

        if printInfo:
            print(f"Octet {i + 1} Entopy: {shannonEntropy}")
            if i == 3:
                print(f"\n\tAverage Entropy: {totalEntropy / 4}\n")

    averageEntropy = totalEntropy / 4

    return averageEntropy


if __name__ == "__main__":
    print(calculateAverageEntropy(
        ["192.168.0.1", "192.168.0.2", "192.168.0.3"]))
    print(calculateAverageEntropy(
        ["192.168.0.1", "130.235.211.41", "2.210.201.41"]))
