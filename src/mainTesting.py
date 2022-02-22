#!/usr/bin/python3

from packetSniff import *
from extractFeatures import *
from trainSVM import trainingTESTING
import pandas as pd
import os

PCAP_MODE = True
ML_TESTING_MODE = not PCAP_MODE


if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("\nError. Programs needs to be run as root.\n")

    if PCAP_MODE:
        outputCSVFile = "csv/ddosTraffic.csv"
    elif ML_TESTING_MODE:
        svmClassifier = trainingTESTING()
    

    while True:
        try:
            fd = open(outputCSVFile, "a")
            trafficFeatures = sniffMininet()
            
            if PCAP_MODE:
                csvWriter = csv.writer(fd)
                csvWriter.writerow(trafficFeatures)
            elif ML_TESTING_MODE:
                featuresML = pd.DataFrame([trafficFeatures])
                featuresML.columns = ["srcIPEntropy", "dstIPEntropy", "packetCount", "avgPacketSize"]

                print(svmClassifier.predict(featuresML))


        except KeyboardInterrupt:
            if PCAP_MODE:
                fd.close()
            
            print("\n\nPacket sniff stopped...\n\n")
            break

        



