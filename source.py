#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
import sys
import time
import json

HOST = '10.10.1.2' # broker ip
PORT = 25574  # port number 

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((HOST,PORT))

# open file to be sent over the network
f = open("./demofile.txt","r")

#set counter
i = 0
total_time = 0
while 1:
    # read 512 bytes from file
    message = f.read(500)
    # if end of file break
    if(len(message) == 0):
        break
    else:
        i += 1
    # if message is valid
    if message:
        s.send(message) # send data
        rcv_data = s.recv(512) # receive destination reply from broker
        f_rcv_data = float(rcv_data) # convert time string to float
        current_time = time.time() # calculate current time
        total_time += current_time-f_rcv_data  # add end-to-end delay to total time.
        # print the end-to-end delay in seconds
        print('sent at :', repr(f_rcv_data), 'received at:',repr(current_time), 'difference:', repr(current_time- f_rcv_data))# print the end-to-end delay
        # calculate avg end-to-end delay in seconds 
        print('avg end-to-end delay for', repr(i), ' packets: '   ,repr(total_time/i))
        
# close tcp socket
s.close()