#!/usr/bin/python3

from packetSniff import *
from extractFeatures import *


if __name__ == "__main__":

    packetCapture = sniffMininet()

    srcIPEntropy = calculateAverageEntropy(packetCapture[0], True)

