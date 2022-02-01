#!/usr/bin/python3

from packetSniff import *
from extractFeatures import *


if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("\nError. Programs needs to be run as root.\n")

    while True:
        try:
            trafficFeatures = sniffMininet()
        except KeyboardInterrupt:
            print("\n\nPacket sniff stopped...\n\n")
            break

        



