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
WINDOW_SIZE = 3
SEGMENT_SIZE = 500

while 1:
    message = ["","",""]
    rcv_data = ["","",""]
    ack_received = [False,False,False]
    # read 512 bytes from file
    for i in range(WINDOW_SIZE):
        message[i] = f.read(SEGMENT_SIZE)
    # if end of file break
    if(len(message[0]) == 0):
        break

    # if message is valid
    if message:

        while not  (ack_received[0] and ack_received[1] and ack_received[2]) :
            for i in range(WINDOW_SIZE):
                print(message[i])
                s.send(message[i]) # send data
                time.sleep(0.1)

            for i in range(WINDOW_SIZE):
                try :
                    rcv_data[i] = s.recv(512) # receive destination reply from broker  !!! MAKE SIZE FIXED !!!!
                    f_rcv_data = float(rcv_data[i]) # convert time string to float
                except :
                    x = 1
                else:
                    print(rcv_data[i])
                    ack_received[i] = True

            
        
# close tcp socket
s.close()