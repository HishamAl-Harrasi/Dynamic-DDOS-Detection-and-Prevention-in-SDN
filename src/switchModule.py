#!/usr/bin/python3

from packetSniff import *
from extractFeatures import *
from trainSVM import SVMtraining
import pandas as pd
import os
import csv
import sys
import argparse
import collections
import subprocess
import re

PCAP_MODE = True
ML_TESTING_MODE = not PCAP_MODE


# Run the mitigation strategy by extracting information from the controller and using it to block the attacker
def mitigateDDOS(switchID):
    inPorts = []
    dstAddresses = []

    result = subprocess.getoutput(
        [f"sudo ovs-ofctl dump-flows s{switchID} --protocol OpenFlow13"])
    subprocess.getoutput(
        [f"sudo ovs-ofctl del-flows s{switchID} --protocol OpenFlow13"])

    flowInfo = result.splitlines()

    for flow in flowInfo:
        inPort = re.search("in_port=(.)", flow)
        dstAddr = re.search("nw_dst=(\d+.\d+.\d+.\d+)", flow)

        if inPort:
            inPorts.append(inPort.group(1))
        if dstAddr:
            dstAddresses.append(dstAddr.group(1))

    attackerPathID = collections.Counter(inPorts).most_common(1)[0][0]
    victimIP = collections.Counter(dstAddresses).most_common(1)[0][0]

    print("----------------------------------------------------------------")
    print(
        f"\nMachine {victimIP} is being attacked through path {attackerPathID}. \n\nMitigating attack now..\n")
    print("----------------------------------------------------------------\n\n")

    subprocess.getoutput([
        f"sudo ovs-ofctl add-flow s1 ip,in_port={attackerPathID},nw_dst={victimIP},priority=100,idle_timeout=10,hard_timeout=25,actions=drop --protocol OpenFlow13"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('switchID', type=int,
                        help='Switch ID of the switch this program is being run on - comes as an integer positional argument after the name of this program')
    args = parser.parse_args()
    switchID = args.switchID

    if os.geteuid() != 0:
        sys.exit("\nError. Programs needs to be run as root.\n")

    if PCAP_MODE:
        outputCSVFile = "testTool.csv"
    elif ML_TESTING_MODE:
        svmClassifier = SVMtraining()

    while True:  # Run infinite loop which sniffs the network and runs the SVM model
        try:
            trafficFeatures = sniffMininet()

            if PCAP_MODE:
                fd = open(outputCSVFile, "a")
                csvWriter = csv.writer(fd)
                csvWriter.writerow(trafficFeatures)
            elif ML_TESTING_MODE:
                featuresML = pd.DataFrame([trafficFeatures])
                featuresML.columns = [
                    "srcIPEntropy", "dstIPEntropy", "packetCount"]

                prediction = svmClassifier.predict(featuresML)

                if prediction == 0:
                    print("Normal Traffic..")
                elif prediction == 1:
                    mitigateDDOS(switchID)

        except KeyboardInterrupt:
            if PCAP_MODE:
                fd.close()

            print("\n\nPacket sniff stopped...\n\n")
            break
