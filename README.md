# Dynamic DDOS Detection & Prevention in SDN

This work is being done as part of my final year project for the degree of Cyber Security BSc at the University of Warwick.


Install the dependancies as specified in the src folder


To run the system:


sudo python3 mininetTopology.py

Then, to test, run a DOS attack in the background from host h1 to host h6:

	h1 hping3 --rand-source --fast h6 &

To run the detection module on the switches run the follwing:

(This will be for switch s1)

	s1 python3 switchModule.py 1                 - the '1' at the end indicates the switch number, if this was s2 then change that to 2
