#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
from threading import Thread
import time
import json


broker_ip_1 = '10.10.1.2' # broker ip
broker_ip_2 = '10.10.2.1' # broker ip
dest_ip_1 = '10.10.3.2' # IP adddress of the destination node
dest_ip_2 = '10.10.5.2' # IP adddress of the destination node
r1_port = 19077 # port number for receiving data from r1
r2_port = 19078 # port number for receiving data from r2

# create and bind socket for receiving data from router1
r1_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r1_udp_sock.bind((dest_ip_1,r1_port))

# create and bind socket for receiving data from router2
r2_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r2_udp_sock.bind((dest_ip_2,r2_port))
FILE = open("output.txt","w")

def internet_checksum(data, sum=0):
    for i in range(0,len(data),2):
        if i + 1 >= len(data):
            sum += ord(data[i]) & 0xFF
        else:
            w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i+1]) & 0xFF)
            sum += w

    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)

    sum = ~sum

    return sum & 0xFFFF


class myThread(Thread): # Thread class 

    #constructor for thread , construct with host and port number
    def __init__(self, HOST, PORT): 
	    Thread.__init__(self)
	    self.HOST = HOST
	    self.PORT = PORT       
    
    def run(self):
        if(self.PORT == 19077):  # if port number reserved for router1
            while 1:
                # receive 512 byte data from router1
                self.data,self.addr = r1_udp_sock.recvfrom(512)
                # if received data is valid
                if self.data:
                    checksum_length = int(self.data[0])
                    checksum_str = self.data[1:checksum_length+1]
                    payload = self.data[checksum_length+1:]
                    flag = internet_checksum(payload,int(checksum_str))                    
                    # send received time as reply to routers   
                    if flag == 0:
                        FILE.write(payload)
                    r1_udp_sock.sendto(str(time.time()),(broker_ip_1,self.PORT))
                    # print received message
                    print('checksum_length: ', checksum_length, 'checksum_str: ', checksum_str, 'flag: ', flag)
                   
                 
                    
        else:   #if port number reserved for router2
            while 1:
                # receive 512 byte data from router2
                self.data,self.addr = r2_udp_sock.recvfrom(512)
                # if received data is valid
                if self.data:  
                    checksum_length = int(self.data[0])
                    checksum_str = self.data[1:checksum_length+1]
                    payload = self.data[checksum_length+1:]
                    flag = internet_checksum(payload,int(checksum_str))
                    # send received time as reply to routers                
                    if flag == 0:
                        FILE.write(payload)
                    r2_udp_sock.sendto(str(time.time()),(broker_ip_2,self.PORT))
                    # print received message
                    print('checksum_length: ', checksum_length, 'checksum_str: ', checksum_str, 'flag:',flag)
                    
        
                    




if __name__ == '__main__': 

    # create thread for router1 socket
    Thread_r1 = myThread(dest_ip_1, r1_port)
    
    # create thread for router2 socket
    Thread_r2 = myThread(dest_ip_2, r2_port)

# Start running the threads
	
    Thread_r1.start()
    Thread_r2.start()

# Close threads
    Thread_r1.join()
    Thread_r2.join()
