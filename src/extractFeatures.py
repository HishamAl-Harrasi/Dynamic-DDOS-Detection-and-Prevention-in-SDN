#!/usr/bin/python3

import sys
import numpy as np
import pandas as pd
import collections



def extractIP(packetCapture):
    ipAddresses = []

    for ip in packetCapture["ip.src"]:
        if type(ip) == str: # CHECK THIS CONDITION !!!!!!!!!!
            ipAddresses.append(ip)
    
    return ipAddresses


def splitIP(ipAddresses):
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
    
def countIPOcurrances(ipOctets):
    firstOctetOccurances = collections.Counter(ipOctets[0])
    secondOctetOccurances = collections.Counter(ipOctets[1])
    thirdOctetOccurances = collections.Counter(ipOctets[2])
    fourthOctetOccurances = collections.Counter(ipOctets[3])

    return [firstOctetOccurances, secondOctetOccurances, thirdOctetOccurances, fourthOctetOccurances]

def calculateAverageEntropy(srcIPAddresses, printInfo = False):
    # Reference: https://stackoverflow.com/questions/27432078/entropy-of-ip-packet-information?rq=1
    srcIPAddrSplit = splitIP(srcIPAddresses)
    octets = countIPOcurrances(srcIPAddrSplit)
    
    totalEntropy = 0

    for i, octet in enumerate(octets):
        counts  = np.array(list(octet.values()))
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
    args = sys.argv[1:]
    df = pd.read_csv(args[0])

    srcIPAddresses = extractIP(df)

    srcIPEntropy = calculateAverageEntropy(srcIPAddresses, True)
