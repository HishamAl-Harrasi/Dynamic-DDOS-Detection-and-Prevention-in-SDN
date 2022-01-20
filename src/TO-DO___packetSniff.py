# from scapy.all import *


import socket
import struct


def extractEthFrame(raw):
    macSrc, macDst, etherType = struct.unpack("! 6s 6s H", raw[:14])
    macSrcStr, macDstStr, etherTypeStr = "", "", ""
    for i, byte in enumerate(macSrc):
        if i <= len(macSrc) - 2:
            macSrcStr += "%02x:" % byte
        else:
            macSrcStr += "%02x" % byte

    for i, byte in enumerate(macDst):
        if i <= len(macDst) - 2:
            macDstStr += "%02x:" % byte
        else:
            macDstStr += "%02x" % byte

    return macSrcStr, macDstStr, raw[14:]    

def extractIPFrame(raw):
# Reference: https://www.uv.mx/personal/angelperez/files/2018/10/sniffers_texto.pdf
    version_header_length = raw[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw[:20])
    data = raw[header_length:]
    # print(socket.inet_ntoa(src))
    # return version, header_length, ttl, proto, src, target, data

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    count = 1
    while True:
        raw, address = s.recvfrom(65565)
        
        macSrc, macDst, raw = extractEthFrame(raw)
        print(macSrc, "", macDst)
        extractIPFrame(raw)
        # print(f"Packet Count: {count}\nSrc: {macSrc}\nDst: {macDst}\n")
        # count += 1
