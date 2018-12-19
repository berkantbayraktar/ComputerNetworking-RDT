#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
from threading import Thread
import time
import json

dest_ip = '10.10.3.2' # IP adddress of the destination node
r1_port = 25572 # port number for receiving data from r1
r2_port = 25573 # port number for receiving data from r2

# create and bind socket for receiving data from router1
r1_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r1_udp_sock.bind((dest_ip,r1_port))

# create and bind socket for receiving data from router2
r2_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r2_udp_sock.bind((dest_ip,r2_port))

class myThread(Thread): # Thread class 

    #constructor for thread , construct with host and port number
    def __init__(self, HOST, PORT): 
	    Thread.__init__(self)
	    self.HOST = HOST
	    self.PORT = PORT       
    
    def run(self):
        if(self.PORT == 25572):  # if port number reserved for router1
            while 1:
                # receive 1024 byte data from router1
                self.data,self.addr = r1_udp_sock.recvfrom(1024)
                # if received data is valid
                if self.data:
                    # send received time as reply to routers
                    r1_udp_sock.sendto(str(time.time()),('10.10.2.2',self.PORT))  
                    # print received message
                    print(self.data)
                   
                 
                    
        else:   #if port number reserved for router2
            while 1:
                # receive 1024 byte data from router2
                self.data,self.addr = r2_udp_sock.recvfrom(1024)
                # if received data is valid
                if self.data:  
                    # send received time as reply to routers
                    r1_udp_sock.sendto(str(time.time()),('10.10.4.2',self.PORT))
                    # print received message
                    print(self.data)
                    
        
                    




if __name__ == '__main__': 

    # create thread for router1 socket
    Thread_r1 = myThread(dest_ip, r1_port)
    
    # create thread for router2 socket
    Thread_r2 = myThread(dest_ip, r2_port)

# Start running the threads
	
    Thread_r1.start()
    Thread_r2.start()

# Close threads
    Thread_r1.join()
    Thread_r2.join()
