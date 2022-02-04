#!/usr/bin/python3

from packetSniff import *
from extractFeatures import *


if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("\nError. Programs needs to be run as root.\n")

    while True:
        try:
            fd = open("csv/normalTraffic.csv", "a")
            trafficFeatures = sniffMininet()
            csvWriter = csv.writer(fd)
            csvWriter.writerow(trafficFeatures)
        except KeyboardInterrupt:
            fd.close()
            print("\n\nPacket sniff stopped...\n\n")
            break

        



